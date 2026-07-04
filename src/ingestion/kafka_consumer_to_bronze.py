import argparse, json
from datetime import datetime
from kafka import KafkaConsumer
from src.common.config import BRONZE, KAFKA_BOOTSTRAP
from src.ingestion.schema_validation import validate_record
TOPIC_TO_DATASET={'logistics.shipments':'shipments','transport.passengers':'passengers','logistics.ports':'ports_operations','transport.rail':'rail_trips','transport.road_incidents':'road_incidents'}
def main(topic: str, max_messages: int=10000):
    dataset=TOPIC_TO_DATASET[topic]; out_dir=BRONZE/dataset; out_dir.mkdir(parents=True,exist_ok=True); out_file=out_dir/f"bronze_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
    consumer=KafkaConsumer(topic,bootstrap_servers=KAFKA_BOOTSTRAP,auto_offset_reset='earliest',consumer_timeout_ms=10000,value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    valid=invalid=0
    with out_file.open('w',encoding='utf-8') as f:
        for i,msg in enumerate(consumer):
            if i>=max_messages: break
            record={k:(None if v=='' else v) for k,v in msg.value.items()}; ok,err=validate_record(dataset,record)
            f.write(json.dumps({'ingestion_ts':datetime.utcnow().isoformat(),'source_topic':topic,'dataset':dataset,'is_valid':ok,'validation_error':err,'payload':record},default=str)+'\n')
            valid+=int(ok); invalid+=int(not ok)
    print(f'Wrote {out_file}. valid={valid}, invalid={invalid}')
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--topic', required=True, choices=list(TOPIC_TO_DATASET.keys())); args=parser.parse_args(); main(args.topic)
