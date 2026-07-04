# AI Knowledge Lakehouse Assistant for Transport & Logistics

منصة ذكاء اصطناعي مؤسسية مستوحاة من NotebookLM لقطاع النقل والخدمات اللوجستية.

#### عمل الفريق: ناديه الغامدي & ابتسام محمد الزهراني & ريناد المطيري 

## Rubric Coverage

| Deliverable | Implementation |
|---|---|
| 1. Kafka producer + consumer with schema validation | `src/ingestion/` + Pydantic schemas |
| 2. Delta Lakehouse bronze/silver/gold with MERGE and schema enforcement | `src/lakehouse/delta_pipeline.py` |
| 3. RAG pipeline: chunking, embedding, vector index, hybrid search, reranking | `src/rag/build_index.py` + `src/rag/query_engine.py` |
| 4. Airflow DAG end-to-end orchestration | `dags/ai_knowledge_lakehouse_dag.py` |
| 5. Great Expectations quality gate + OpenLineage events | `src/quality/great_expectations_checks.py` + `src/quality/openlineage_emit.py` |

## Features

- Real embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- FAISS vector index for semantic retrieval.
- Hybrid search: FAISS dense retrieval + BM25 lexical search.
- Reranking by term overlap.
- Real Great Expectations execution.
- OpenLineage-compatible event emission.
- Delta Lakehouse with Bronze/Silver/Gold and MERGE logic.
- Airflow DAG connecting the full pipeline.

## Quick Start

```bash
pip install -r requirements.txt

python src/data/generate_synthetic_data.py
python src/lakehouse/delta_pipeline.py
python src/quality/great_expectations_checks.py
python src/rag/build_index.py
streamlit run src/app/streamlit_app.py
```

Kafka optional:

```bash
docker compose up -d kafka zookeeper
python src/ingestion/kafka_producer.py --dataset shipments
python src/ingestion/kafka_consumer_to_bronze.py --topic logistics.shipments
```

## AI Assistant Streamlit & some Demo Questions
(assets/assistant-preview.png)[واجهة المساعد الذكي]!

- ما هو SLA الخاص بتحديث بيانات الشحنات؟
- ما هي مؤشرات النقل البحري الموجودة في الكتالوج؟
- لخص سياسة جودة البيانات.
- ما هي طبقات Lakehouse في هذا المشروع؟
- اكتب تقريرًا تنفيذيًا عن جودة البيانات.
