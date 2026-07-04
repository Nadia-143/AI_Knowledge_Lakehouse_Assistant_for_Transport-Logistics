from pathlib import Path
from datetime import datetime, timedelta
import random, pandas as pd
ROOT = Path(__file__).resolve().parents[2]
RAW, REF, DOCS = ROOT/'data/raw', ROOT/'data/reference', ROOT/'data/documents'
for p in [RAW, REF, DOCS]: p.mkdir(parents=True, exist_ok=True)
random.seed(42); AGENCIES=['GACA','Mawani','SAR','RGA','TGA','SPL','MOTLS']; REGIONS=['Riyadh','Makkah','Madinah','Eastern','Asir','Tabuk','Qassim','Jazan']; BASE=datetime(2025,1,1)
def rand_date(days=180): return BASE+timedelta(days=random.randint(0,days))
def maybe_missing(v,p=0.04): return None if random.random()<p else v
def generate_shipments(n=1000):
    rows=[]
    for i in range(n):
        planned=rand_date(); delay=random.choice([-2,-1,0,1,2,3,5,7,10]); status=random.choices(['Delivered','In Transit','Delayed','Cancelled'], weights=[70,15,12,3])[0]; actual=planned+timedelta(days=max(delay,0)) if status in ['Delivered','Delayed'] else None
        rows.append({'shipment_id':f'SHP-{i:06d}','agency':random.choice(['Mawani','SPL','TGA']),'origin_region':maybe_missing(random.choice(REGIONS)),'destination_region':random.choice(REGIONS),'mode':random.choice(['Sea','Road','Logistics']),'shipment_status':status,'planned_delivery_date':planned.date().isoformat(),'actual_delivery_date':actual.date().isoformat() if actual else None,'weight_tons':round(random.uniform(0.5,80),2),'cost_sar':round(random.uniform(500,50000),2)})
    pd.DataFrame(rows).to_csv(RAW/'shipments.csv',index=False)
def generate_passengers(n=1000):
    rows=[{'record_id':f'PSG-{i:06d}','agency':random.choice(['GACA','SAR','TGA']),'mode':random.choice(['Air','Rail','Road']),'region':maybe_missing(random.choice(REGIONS)),'travel_date':rand_date().date().isoformat(),'passengers_count':random.randint(50,12000),'satisfaction_score':round(random.uniform(2.5,5.0),2)} for i in range(n)]
    pd.DataFrame(rows).to_csv(RAW/'passengers.csv',index=False)
def generate_ports(n=600):
    ports=['Jeddah Islamic Port','King Abdulaziz Port','King Abdullah Port','Jazan Port']; rows=[]
    for i in range(n): rows.append({'operation_id':f'PORT-{i:06d}','agency':'Mawani','port_name':random.choice(ports),'operation_date':rand_date().date().isoformat(),'containers_handled':random.randint(100,8000),'vessel_waiting_hours':round(random.uniform(0.5,48),2),'berth_occupancy_rate':round(random.uniform(45,98),2)})
    pd.DataFrame(rows).to_csv(RAW/'ports_operations.csv',index=False)
def generate_rail(n=700):
    lines=['Riyadh-Dammam','Haramain','North Train','Riyadh-Qassim']; rows=[]
    for i in range(n):
        delay=random.choices([0,5,10,15,30,60,90], weights=[55,12,12,8,6,5,2])[0]; rows.append({'trip_id':f'RAIL-{i:06d}','agency':'SAR','line_name':random.choice(lines),'trip_date':rand_date().date().isoformat(),'on_time_flag':delay<=10,'delay_minutes':delay,'passengers_count':random.randint(20,1000)})
    pd.DataFrame(rows).to_csv(RAW/'rail_trips.csv',index=False)
def generate_road(n=600):
    rows=[{'incident_id':f'ROAD-{i:06d}','agency':random.choice(['RGA','MOTLS']),'region':random.choice(REGIONS),'incident_date':rand_date().date().isoformat(),'severity':random.choice(['Low','Medium','High']),'road_type':random.choice(['Highway','Urban','Rural']),'clearance_minutes':random.randint(10,240)} for i in range(n)]
    pd.DataFrame(rows).to_csv(RAW/'road_incidents.csv',index=False)
def generate_reference():
    kpis=[['KPI-001','Average Shipment Delay Days','Logistics','Average actual delivery delay in days','days','shipments','monthly','Mawani/SPL/TGA'],['KPI-002','On-Time Rail Trip Rate','Rail','Percentage of rail trips arriving on time','%','rail_trips','monthly','SAR'],['KPI-003','Passenger Satisfaction Score','Multi-modal','Average satisfaction score across modes','score','passengers','quarterly','GACA/SAR/TGA'],['KPI-004','Containers Handled','Sea','Total containers handled across ports','containers','ports_operations','monthly','Mawani'],['KPI-005','Vessel Waiting Hours','Sea','Average waiting time for vessels','hours','ports_operations','monthly','Mawani'],['KPI-006','Road Incident Clearance Time','Road','Average time to clear road incidents','minutes','road_incidents','monthly','RGA'],['KPI-007','Data Freshness Compliance','Governance','Percentage of datasets updated within SLA','%','all','monthly','All agencies'],['KPI-008','Data Quality Score','Governance','Composite score based on completeness, validity, duplicates','%','all','monthly','All agencies']]
    pd.DataFrame(kpis,columns=['kpi_id','kpi_name','domain','definition','unit','source_dataset','frequency','data_owner']).to_csv(REF/'transport_kpi_catalog.csv',index=False)
    sla=[]
    for dataset in ['shipments','passengers','ports_operations','rail_trips','road_incidents']:
        sla.append({'sla_id':f'SLA-{dataset.upper()}','dataset_name':dataset,'owner_agency':random.choice(AGENCIES),'expected_frequency':random.choice(['daily','weekly','monthly']),'submission_due_day':random.randint(3,10),'max_allowed_delay_days':random.choice([1,2,3,5]),'minimum_quality_score':random.choice([85,90,95]),'escalation_level_1':'Data Steward','escalation_level_2':'Data Governance Lead','penalty_note':'Requires corrective action plan if SLA is breached twice in a quarter.'})
    pd.DataFrame(sla).to_csv(REF/'sla_templates.csv',index=False)
def generate_documents():
    policy='\n'.join(['# Transport Data Governance Policy','','## Data Quality Dimensions','- Completeness: mandatory fields should not be missing.','- Accuracy: values should reflect operational reality.','- Consistency: definitions should match the approved KPI catalog.','- Timeliness: datasets should be submitted according to SLA.','- Uniqueness: duplicate records should be minimized.','','## Lakehouse Zones','Bronze stores raw ingested data.','Silver stores cleaned and standardized data.','Gold stores curated KPI tables and reporting datasets.'])
    sla='\n'.join(['# SLA Operating Model','','Each agency must submit datasets based on the agreed frequency.','Monthly datasets must be submitted before the due day defined in the SLA template.','If a dataset is late, the platform marks it as SLA breach.','If quality score is below the minimum threshold, the dataset is rejected by the quality gate.','','Escalation:','1. Notify Data Steward.','2. Notify Data Governance Lead.','3. Request corrective action plan.'])
    (DOCS/'data_governance_policy.md').write_text(policy,encoding='utf-8'); (DOCS/'sla_operating_model.md').write_text(sla,encoding='utf-8')
def main():
    generate_shipments(); generate_passengers(); generate_ports(); generate_rail(); generate_road(); generate_reference(); generate_documents(); print('Synthetic transport & logistics data generated.')
if __name__=='__main__': main()
