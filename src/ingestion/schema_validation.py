from pydantic import ValidationError
from src.common.schemas import ShipmentEvent, PassengerRecord, PortOperation, RailTrip, RoadIncident
SCHEMA_MAP={'shipments':ShipmentEvent,'passengers':PassengerRecord,'ports_operations':PortOperation,'rail_trips':RailTrip,'road_incidents':RoadIncident}
def validate_record(dataset: str, record: dict) -> tuple[bool, str]:
    model=SCHEMA_MAP.get(dataset)
    if model is None: return False, f'Unknown dataset: {dataset}'
    try: model(**record); return True, ''
    except ValidationError as e: return False, e.json()
