import json, pandas as pd
from datetime import datetime
from src.common.config import RAW, GOLD
from src.quality.openlineage_emit import emit_lineage_event
def compute_quality_score(df):
    total=max(df.shape[0]*df.shape[1],1); missing=df.isna().sum().sum()/total; dup=df.duplicated().sum()/max(len(df),1); score=max(0,100-(missing*60+dup*40)*100)
    return {'row_count':len(df),'column_count':len(df.columns),'missing_rate':round(missing,4),'duplicate_rate':round(dup,4),'quality_score':round(score,2),'status':'PASS' if score>=85 else 'FAIL'}
def run_great_expectations_on_dataframe(df,dataset):
    import great_expectations as ge
    ge_df=ge.from_pandas(df); results=[ge_df.expect_table_row_count_to_be_between(min_value=1)]
    if 'agency' in df.columns: results.append(ge_df.expect_column_values_to_not_be_null('agency'))
    if dataset=='shipments': results += [ge_df.expect_column_values_to_be_between('weight_tons',min_value=0),ge_df.expect_column_values_to_be_between('cost_sar',min_value=0),ge_df.expect_column_values_to_be_in_set('shipment_status',['Delivered','In Transit','Delayed','Cancelled'])]
    elif dataset=='passengers': results += [ge_df.expect_column_values_to_be_between('passengers_count',min_value=0),ge_df.expect_column_values_to_be_between('satisfaction_score',min_value=1,max_value=5)]
    elif dataset=='ports_operations': results += [ge_df.expect_column_values_to_be_between('containers_handled',min_value=0),ge_df.expect_column_values_to_be_between('berth_occupancy_rate',min_value=0,max_value=100)]
    elif dataset=='rail_trips': results += [ge_df.expect_column_values_to_be_between('delay_minutes',min_value=0),ge_df.expect_column_values_to_be_between('passengers_count',min_value=0)]
    elif dataset=='road_incidents': results += [ge_df.expect_column_values_to_be_between('clearance_minutes',min_value=0),ge_df.expect_column_values_to_be_in_set('severity',['Low','Medium','High'])]
    passed=sum(1 for r in results if bool(r.get('success')))
    return {'ge_executed':True,'ge_success':passed==len(results),'ge_expectations_total':len(results),'ge_expectations_passed':passed,'ge_results':[{'expectation':r.get('expectation_config',{}).get('expectation_type','unknown'),'success':bool(r.get('success'))} for r in results]}
def main():
    results=[]; details=[]
    for file in RAW.glob('*.csv'):
        dataset=file.stem; df=pd.read_csv(file); score=compute_quality_score(df); ge_result=run_great_expectations_on_dataframe(df,dataset)
        results.append({'dataset':dataset,**score,'ge_executed':ge_result['ge_executed'],'ge_success':ge_result['ge_success'],'ge_expectations_total':ge_result['ge_expectations_total'],'ge_expectations_passed':ge_result['ge_expectations_passed'],'validation_ts':datetime.utcnow().isoformat()})
        details.append({'dataset':dataset,'file':str(file),'result':ge_result})
    GOLD.mkdir(parents=True,exist_ok=True); metrics_out=GOLD/'quality_metrics.csv'; details_out=GOLD/'great_expectations_validation_results.json'
    pd.DataFrame(results).to_csv(metrics_out,index=False); details_out.write_text(json.dumps(details,indent=2,default=str),encoding='utf-8')
    emit_lineage_event('great_expectations_quality_gate',[str(p) for p in RAW.glob('*.csv')],[str(metrics_out),str(details_out)])
    print(pd.DataFrame(results))
if __name__=='__main__': main()
