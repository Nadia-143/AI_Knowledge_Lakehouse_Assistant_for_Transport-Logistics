from pathlib import Path
from pyspark.sql import SparkSession, functions as F
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from src.common.config import RAW, BRONZE, SILVER, GOLD
def get_spark():
    builder=(SparkSession.builder.appName('AI-Knowledge-Lakehouse').config('spark.sql.extensions','io.delta.sql.DeltaSparkSessionExtension').config('spark.sql.catalog.spark_catalog','org.apache.spark.sql.delta.catalog.DeltaCatalog'))
    return configure_spark_with_delta_pip(builder).getOrCreate()
def write_bronze_from_csv(spark,dataset):
    df=spark.read.option('header',True).option('inferSchema',True).csv(str(RAW/f'{dataset}.csv')).withColumn('_ingestion_ts',F.current_timestamp()).withColumn('_source_file',F.lit(f'{dataset}.csv'))
    df.write.format('delta').mode('overwrite').option('overwriteSchema','true').save(str(BRONZE/dataset))
def standardize_silver(spark,dataset):
    df=spark.read.format('delta').load(str(BRONZE/dataset))
    for c in df.columns:
        if c.endswith('_date'): df=df.withColumn(c,F.to_date(F.col(c)))
        if c in ['agency','mode','region','origin_region','destination_region','shipment_status']: df=df.withColumn(c,F.trim(F.col(c)))
    df.dropDuplicates().withColumn('_silver_processed_ts',F.current_timestamp()).write.format('delta').mode('overwrite').option('overwriteSchema','true').save(str(SILVER/dataset))
def merge_gold_table(spark, df, path: Path, keys):
    if DeltaTable.isDeltaTable(spark,str(path)):
        cond=' AND '.join([f'target.{k}=source.{k}' for k in keys]); DeltaTable.forPath(spark,str(path)).alias('target').merge(df.alias('source'),cond).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    else: df.write.format('delta').mode('overwrite').save(str(path))
def build_gold_kpis(spark):
    shipments=spark.read.format('delta').load(str(SILVER/'shipments')); rail=spark.read.format('delta').load(str(SILVER/'rail_trips')); passengers=spark.read.format('delta').load(str(SILVER/'passengers')); ports=spark.read.format('delta').load(str(SILVER/'ports_operations')); road=spark.read.format('delta').load(str(SILVER/'road_incidents'))
    shipment_kpi=shipments.withColumn('delay_days',F.datediff('actual_delivery_date','planned_delivery_date')).withColumn('delay_days',F.when(F.col('delay_days')<0,0).otherwise(F.col('delay_days'))).groupBy('agency','mode').agg(F.count('*').alias('shipment_count'),F.avg('delay_days').alias('avg_delay_days'),F.sum(F.when(F.col('shipment_status')=='Delayed',1).otherwise(0)).alias('delayed_shipments'))
    rail_kpi=rail.groupBy('agency','line_name').agg(F.count('*').alias('trip_count'),F.avg(F.col('on_time_flag').cast('double')).alias('on_time_rate'),F.avg('delay_minutes').alias('avg_delay_minutes'))
    passenger_kpi=passengers.groupBy('agency','mode','region').agg(F.sum('passengers_count').alias('total_passengers'),F.avg('satisfaction_score').alias('avg_satisfaction_score'))
    port_kpi=ports.groupBy('agency','port_name').agg(F.sum('containers_handled').alias('containers_handled'),F.avg('vessel_waiting_hours').alias('avg_vessel_waiting_hours'),F.avg('berth_occupancy_rate').alias('avg_berth_occupancy_rate'))
    road_kpi=road.groupBy('agency','region','severity').agg(F.count('*').alias('incident_count'),F.avg('clearance_minutes').alias('avg_clearance_minutes'))
    merge_gold_table(spark,shipment_kpi,GOLD/'kpi_shipments',['agency','mode']); merge_gold_table(spark,rail_kpi,GOLD/'kpi_rail',['agency','line_name']); merge_gold_table(spark,passenger_kpi,GOLD/'kpi_passengers',['agency','mode','region']); merge_gold_table(spark,port_kpi,GOLD/'kpi_ports',['agency','port_name']); merge_gold_table(spark,road_kpi,GOLD/'kpi_road',['agency','region','severity'])
def main():
    spark=get_spark()
    for ds in ['shipments','passengers','ports_operations','rail_trips','road_incidents']: write_bronze_from_csv(spark,ds); standardize_silver(spark,ds)
    build_gold_kpis(spark); spark.stop(); print('Delta Lakehouse created: bronze/silver/gold')
if __name__=='__main__': main()
