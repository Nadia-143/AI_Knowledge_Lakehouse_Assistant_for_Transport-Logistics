# Transport Data Governance Policy

## Data Quality Dimensions
- Completeness: mandatory fields should not be missing.
- Accuracy: values should reflect operational reality.
- Consistency: definitions should match the approved KPI catalog.
- Timeliness: datasets should be submitted according to SLA.
- Uniqueness: duplicate records should be minimized.

## Lakehouse Zones
Bronze stores raw ingested data.
Silver stores cleaned and standardized data.
Gold stores curated KPI tables and reporting datasets.