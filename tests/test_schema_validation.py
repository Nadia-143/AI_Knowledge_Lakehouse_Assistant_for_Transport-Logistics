from src.ingestion.schema_validation import validate_record
def test_valid_shipment_schema():
    record={'shipment_id':'SHP-1','agency':'Mawani','origin_region':'Riyadh','destination_region':'Makkah','mode':'Road','shipment_status':'Delivered','planned_delivery_date':'2025-01-01','actual_delivery_date':'2025-01-02','weight_tons':10.5,'cost_sar':4000.0}
    ok,err=validate_record('shipments',record); assert ok, err
def test_invalid_negative_weight():
    record={'shipment_id':'SHP-2','agency':'Mawani','origin_region':'Riyadh','destination_region':'Makkah','mode':'Road','shipment_status':'Delivered','planned_delivery_date':'2025-01-01','actual_delivery_date':'2025-01-02','weight_tons':-1,'cost_sar':4000.0}
    ok,err=validate_record('shipments',record); assert not ok
