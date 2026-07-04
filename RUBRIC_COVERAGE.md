# Rubric Coverage Evidence

## Deliverable 1 — Kafka Ingestion + Schema Validation
Files: `src/ingestion/kafka_producer.py`, `src/ingestion/kafka_consumer_to_bronze.py`, `src/ingestion/schema_validation.py`, `src/common/schemas.py`.

Evidence: Producer publishes records to Kafka topics. Consumer validates each event using Pydantic schemas and writes validation envelopes to Bronze.

## Deliverable 2 — Delta Lakehouse Bronze/Silver/Gold + MERGE
File: `src/lakehouse/delta_pipeline.py`.

Evidence: Bronze raw Delta tables, Silver standardized Delta tables, Gold curated KPI Delta tables, MERGE through `DeltaTable.merge`, and schema enforcement through Delta and casting.

## Deliverable 3 — RAG Pipeline
Files: `src/rag/build_index.py`, `src/rag/query_engine.py`.

Evidence: chunking, real embedding model `sentence-transformers/all-MiniLM-L6-v2`, FAISS vector index, BM25 lexical index, hybrid retrieval, and reranking by term overlap.

## Deliverable 4 — Airflow Orchestration
File: `dags/ai_knowledge_lakehouse_dag.py`.

Evidence: DAG connects generation → lakehouse → quality → RAG.

## Deliverable 5 — Quality Gate + OpenLineage
Files: `src/quality/great_expectations_checks.py`, `src/quality/openlineage_emit.py`, `expectations/transport_quality_suite.json`.

Evidence: Great Expectations runs on raw datasets, quality metrics are written, and OpenLineage-compatible events are emitted.
