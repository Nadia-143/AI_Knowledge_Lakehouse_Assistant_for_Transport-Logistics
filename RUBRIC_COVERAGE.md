# Rubric Coverage Evidence

## Deliverable 1 — Kafka Ingestion + Schema Validation
Files: `src/ingestion/kafka_producer.py`, `src/ingestion/kafka_consumer_to_bronze.py`, `src/ingestion/schema_validation.py`, `src/common/schemas.py`.

Evidence: Kafka producer and consumer scripts were implemented as an optional streaming ingestion layer. The producer simulates logistics events, while the consumer validates each event using Pydantic schemas and writes validation envelopes to the Bronze layer.

** Kafka is optional because the core pipeline can also run using generated batch data, ensuring the project remains reproducible even when a Kafka runtime is not available.**

## Deliverable 2 — Delta Lakehouse Bronze/Silver/Gold + MERGE
File: `src/lakehouse/delta_pipeline.py`.

Evidence: Bronze raw Delta tables, Silver standardized Delta tables, Gold curated KPI Delta tables, MERGE through `DeltaTable.merge`, and schema enforcement through Delta and casting.

## Deliverable 3 — RAG Pipeline
Files: `src/rag/build_index.py`, `src/rag/query_engine.py`, `data/knowledge/project_knowledge_base.md`.
Evidence: The RAG pipeline supports document chunking, embedding generation using `sentence-transformers/all-MiniLM-L6-v2`, FAISS vector indexing, BM25 lexical search, hybrid retrieval, and reranking by term overlap.

** A project knowledge base file was added under `data/knowledge/` to provide the assistant with grounded information about the Lakehouse architecture, data sources, SLA definitions, Kafka role, Docker role, and RAG behavior. The assistant only answers based on indexed knowledge and returns a clear fallback message when no relevant context is found. **

## Deliverable 4 — Airflow Orchestration
File: `dags/ai_knowledge_lakehouse_dag.py`.

Evidence: DAG connects generation → lakehouse → quality → RAG.

## Deliverable 5 — Quality Gate + OpenLineage
Files: `src/quality/great_expectations_checks.py`, `src/quality/openlineage_emit.py`, `expectations/transport_quality_suite.json`.

Evidence: Great Expectations runs on raw datasets, quality metrics are written, and OpenLineage-compatible events are emitted.

## Deliverable 6 — Streamlit AI Assistant Interface
Files: `src/app/streamlit_app.py`, `src/app/sdaia_logo.png`, `assets/assistant-preview.png`.

Evidence: A Streamlit-based Arabic user interface was implemented for the AI Knowledge Lakehouse Assistant. The interface includes a chatbot-style layout, SDAIA branding, Arabic RTL design, team information, data source summary, and a question/answer panel connected to the RAG query engine.


The UI is designed to demonstrate how business users can interact with the Lakehouse knowledge layer through a simple assistant interface.
