from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
class ShipmentEvent(BaseModel):
    shipment_id: str; agency: str; origin_region: str; destination_region: str; mode: str; shipment_status: str; planned_delivery_date: date; actual_delivery_date: Optional[date]; weight_tons: float = Field(ge=0); cost_sar: float = Field(ge=0)
class PassengerRecord(BaseModel):
    record_id: str; agency: str; mode: str; region: str; travel_date: date; passengers_count: int = Field(ge=0); satisfaction_score: float = Field(ge=1, le=5)
class PortOperation(BaseModel):
    operation_id: str; agency: str; port_name: str; operation_date: date; containers_handled: int = Field(ge=0); vessel_waiting_hours: float = Field(ge=0); berth_occupancy_rate: float = Field(ge=0, le=100)
class RailTrip(BaseModel):
    trip_id: str; agency: str; line_name: str; trip_date: date; on_time_flag: bool; delay_minutes: int = Field(ge=0); passengers_count: int = Field(ge=0)
class RoadIncident(BaseModel):
    incident_id: str; agency: str; region: str; incident_date: date; severity: str; road_type: str; clearance_minutes: int = Field(ge=0)
