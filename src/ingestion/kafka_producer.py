import argparse, json, pandas as pd
from kafka import KafkaProducer
from src.common.config import RAW, KAFKA_BOOTSTRAP
TOPICS={'shipments':'logistics.shipments','passengers':'transport.passengers','ports_operations':'logistics.ports','rail_trips':'transport.rail','road_incidents':'transport.road_incidents'}
def main(dataset: str):
    producer=KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP,value_serializer=lambda v: json.dumps(v,default=str).encode('utf-8'))
    df=pd.read_csv(RAW/f'{dataset}.csv').fillna('')
    for _,row in df.iterrows(): producer.send(TOPICS[dataset], row.to_dict())
    producer.flush(); print(f'Sent {len(df)} records to {TOPICS[dataset]}')
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--dataset', required=True, choices=list(TOPICS.keys())); args=parser.parse_args(); main(args.dataset)
