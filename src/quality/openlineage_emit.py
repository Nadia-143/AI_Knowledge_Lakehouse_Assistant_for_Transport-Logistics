from datetime import datetime
import json
from src.common.config import GOLD
def emit_lineage_event(job_name, inputs, outputs, status='COMPLETE'):
    event={'eventType':status,'eventTime':datetime.utcnow().isoformat()+'Z','job':{'namespace':'ai-knowledge-lakehouse','name':job_name},'run':{'runId':f"{job_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"},'inputs':[{'namespace':'local','name':x} for x in inputs],'outputs':[{'namespace':'local','name':x} for x in outputs],'producer':'ai-knowledge-lakehouse-assistant'}
    out=GOLD/'openlineage_events.jsonl'; out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('a',encoding='utf-8') as f: f.write(json.dumps(event)+'\n')
    return event
