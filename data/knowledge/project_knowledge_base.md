# AI Knowledge Lakehouse Assistant for Transport & Logistics
## Project Overview
The AI Knowledge Lakehouse Assistant is an intelligent knowledge assistant designed for the transport and logistics sector. The project simulates an enterprise data platform that combines modern data engineering, Lakehouse architecture, data quality validation, SLA monitoring, and Retrieval-Augmented Generation (RAG).
The assistant helps users ask questions about logistics data, operational indicators, data quality, Lakehouse layers, SLA definitions, Kafka ingestion, Docker usage, and project architecture.
The project is designed for the transport and logistics domain and uses synthetic data to simulate real enterprise scenarios.
---
## Project Objective
The main objective of the project is to build an integrated and scalable AI data platform that can:
- Ingest transport and logistics data.
- Validate incoming data using schemas.
- Store and process data using Lakehouse layers.
- Apply data quality checks.
- Build a searchable knowledge base.
- Enable users to ask questions through an AI assistant interface.
- Support batch and optional streaming ingestion patterns.
- Demonstrate a production-like architecture using Python, PySpark, Delta Lake, RAG, Streamlit, Kafka, Airflow, and Great Expectations.
---
## Transport and Logistics Domain
The project focuses on the transport and logistics sector. The simulated data represents operational activities across different modes of transport and logistics services.
The domain includes:
- Shipments.
- Ports.
- Rail trips.
- Road incidents.
- Passenger data.
- SLA templates.
- KPI catalog.
- Logistics operations.
- Transport performance indicators.
---
## Data Sources
The project uses synthetic data sources to simulate real-world transport and logistics datasets.
The main data sources are:
1. Shipment data.
2. Port operations data.
3. Railway trip data.
4. Road incident data.
5. Passenger data.
6. KPI catalog.
7. SLA templates.
These datasets are used to simulate data ingestion, data validation, Lakehouse processing, quality checks, and RAG knowledge retrieval.
---
## Lakehouse Architecture
The project follows a Lakehouse architecture using the Medallion pattern.
The Medallion architecture consists of three main layers:
1. Bronze Layer.
2. Silver Layer.
3. Gold Layer.
Each layer has a specific purpose in the data lifecycle.
---
## Bronze Layer
The Bronze Layer stores raw data.
In this project, the Bronze Layer represents the first landing zone for ingested data. Data is stored with minimal transformation to preserve its original structure.
Examples of Bronze data include:
- Raw shipment records.
- Raw port operation events.
- Raw rail trip records.
- Raw road incident records.
- Raw passenger data.
- Raw Kafka event envelopes.
The Bronze Layer is useful for traceability, auditing, and replaying data pipelines when needed.
---
## Silver Layer
The Silver Layer stores cleaned and standardized data.
In this project, the Silver Layer applies data cleaning, type casting, deduplication, schema enforcement, and standardization.
Typical Silver Layer processing includes:
- Removing duplicate records.
- Handling missing values.
- Standardizing column names.
- Validating data types.
- Casting date and numeric fields.
- Filtering invalid records.
- Applying schema validation rules.
The Silver Layer prepares reliable data for analytics and downstream processing.
---
## Gold Layer
The Gold Layer stores curated analytical data.
In this project, the Gold Layer prepares business-ready datasets for dashboards, SLA monitoring, KPI reporting, and AI assistant retrieval.
Examples of Gold outputs include:
- KPI summary tables.
- SLA compliance summaries.
- Shipment performance indicators.
- Port operation metrics.
- Rail performance metrics.
- Road incident indicators.
- Aggregated transport and logistics metrics.
The Gold Layer is the preferred layer for business consumption, analytics, dashboards, and AI applications.
---
## Delta Lake
Delta Lake is used in the project to support reliable Lakehouse processing.
Delta Lake provides:
- ACID transactions.
- Schema enforcement.
- Schema evolution.
- Merge operations.
- Reliable updates.
- Scalable data storage.
- Bronze, Silver, and Gold data management.
In the project, Delta Lake is used to create and manage the Lakehouse pipeline.
---
## MERGE Operation
The project uses Delta Lake MERGE logic to update or insert records into Delta tables.
MERGE is useful when the pipeline needs to:
- Insert new records.
- Update existing records.
- Avoid duplicate records.
- Apply incremental loading.
- Maintain reliable curated tables.
---
## Schema Validation
Schema validation ensures that incoming data follows expected structures and data types.
In this project, schema validation is implemented using Pydantic schemas.
Schema validation checks whether each record contains the required fields and whether each field has the correct type.
Examples of schema validation checks include:
- Shipment ID must exist.
- Event timestamp must be valid.
- Transport mode must be valid.
- Numeric fields must contain numeric values.
- Required fields must not be missing.
Invalid records can be rejected, flagged, or written into validation envelopes.
---
## Pydantic
Pydantic is used for schema validation in the ingestion layer.
It validates data records against predefined Python schemas.
In this project, Pydantic helps ensure that logistics events and generated records follow the expected data structure before they are written to the Lakehouse.
---
## Kafka
Kafka is used as an optional streaming ingestion layer.
Kafka is not required for the core execution of the project. The project can run using generated batch data without Kafka.
Kafka is included to demonstrate how the platform could support real-time or near-real-time logistics events.
Examples of Kafka events include:
- Shipment status updates.
- Vehicle movement events.
- Port operation events.
- Rail trip updates.
- Incident alerts.
---
## Why Kafka Is Optional
Kafka is optional because the core project should remain reproducible and easy to run.
Running Kafka requires additional infrastructure, brokers, ports, and runtime configuration. To make the project easier to execute in training or demo environments, the batch pipeline can run independently without Kafka.
This design shows good engineering practice because the project supports two ingestion modes:
1. Batch ingestion using generated synthetic data.
2. Optional streaming ingestion using Kafka.
The core pipeline does not depend on Kafka to function.
---
## Kafka Producer
The Kafka producer simulates logistics events and publishes them to Kafka topics.
The producer represents systems that send operational events, such as shipment tracking systems, port systems, or transport monitoring systems.
---
## Kafka Consumer
The Kafka consumer reads events from Kafka topics.
In this project, the consumer validates each event using Pydantic schemas and writes validated or rejected records into the Bronze layer.
---
## Docker
Docker is used to run services in isolated containers.
Docker helps run tools such as Kafka and other supporting services without installing them manually on the local machine.
In this project, Docker supports reproducible infrastructure and makes it easier to simulate enterprise environments.
Docker does not replace Kafka. Docker runs services, while Kafka streams data.
---
## Difference Between Docker and Kafka
Docker is used to run and package services.
Kafka is used to stream data.
Docker can be used to run Kafka, but they are not the same thing.
In simple terms:
- Docker runs the environment.
- Kafka moves real-time data.
- Delta Lake stores and processes the data.
- Streamlit displays the assistant interface.
- RAG retrieves knowledge and generates answers.
---
## Airflow
Airflow is used for workflow orchestration.
In this project, Airflow can orchestrate the end-to-end pipeline, including:
- Synthetic data generation.
- Lakehouse processing.
- Data quality checks.
- RAG index building.
- Pipeline execution order.
Airflow helps automate and schedule the data pipeline.
---
## Great Expectations
Great Expectations is used for data quality validation.
In this project, it checks whether datasets meet expected quality rules.
Examples of data quality checks include:
- Required columns exist.
- Values are not null.
- Numeric values are within valid ranges.
- Dates are valid.
- Categories follow expected values.
- Duplicates are controlled.
Great Expectations helps ensure that the data is reliable before it is used by dashboards or the AI assistant.
---
## OpenLineage
OpenLineage is used to emit lineage-related events.
Lineage helps track how data moves through the pipeline.
In this project, OpenLineage-compatible events can describe:
- Which pipeline ran.
- Which datasets were used.
- Which datasets were produced.
- Which quality checks were executed.
- How data moved from source to Bronze, Silver, and Gold layers.
---
## Data Quality
Data quality is a critical part of the project.
The project validates data quality to ensure that the assistant and analytics outputs are based on reliable data.
Main data quality dimensions include:
- Completeness.
- Validity.
- Accuracy.
- Consistency.
- Uniqueness.
- Timeliness.
Data quality issues may include:
- Missing values.
- Duplicate records.
- Invalid dates.
- Negative durations.
- Invalid transport modes.
- Incorrect SLA values.
- Inconsistent IDs.
---
## SLA
SLA stands for Service Level Agreement.
In this project, SLA is used to measure whether transport and logistics services meet expected performance thresholds.
Examples of SLA metrics include:
- Shipment processing time.
- Delivery delay time.
- Incident response time.
- Port handling time.
- Rail trip delay.
- Service availability.
- Data refresh timeliness.
SLA monitoring helps identify whether operations are meeting expected service levels.
---
## KPI Catalog
The KPI catalog defines the key performance indicators used in the project.
Examples of KPIs include:
- Total shipments.
- On-time delivery rate.
- Average shipment delay.
- Port throughput.
- Rail punctuality.
- Road incident count.
- Passenger volume.
- SLA compliance rate.
- Data quality score.
The KPI catalog supports analytics, dashboards, and AI assistant responses.
---
## RAG
RAG stands for Retrieval-Augmented Generation.
In this project, RAG allows the assistant to answer questions using indexed project knowledge and data documentation.
RAG works by:
1. Receiving a user question.
2. Searching indexed knowledge sources.
3. Retrieving the most relevant chunks.
4. Passing the retrieved context to the answer engine.
5. Returning an answer based on the retrieved context.
The assistant should not invent answers. If no relevant context is found, it should return a clear message saying that no related answer was found in the available data sources.
---
## RAG Pipeline
The RAG pipeline includes:
- Document loading.
- Text chunking.
- Embedding generation.
- FAISS vector indexing.
- BM25 lexical search.
- Hybrid retrieval.
- Reranking.
- Query answering.
The project uses sentence-transformers embeddings and FAISS for semantic search.
---
## Embeddings
Embeddings convert text into numerical vectors.
In this project, embeddings are used to represent knowledge documents so that the assistant can search for semantically similar content.
The project uses a sentence-transformers model such as all-MiniLM-L6-v2 for embedding generation.
---
## FAISS
FAISS is used as a vector index.
It enables fast semantic search across embedded chunks of project knowledge.
When the user asks a question, FAISS helps retrieve the most semantically relevant content.
---
## BM25
BM25 is a lexical search method.
It searches based on keyword matching.
In this project, BM25 can complement FAISS semantic search by improving retrieval when the question contains important exact terms such as Kafka, SLA, Bronze, Silver, Gold, or RAG.
---
## Hybrid Search
Hybrid search combines semantic retrieval and lexical retrieval.
In this project, hybrid search may use:
- FAISS for semantic similarity.
- BM25 for keyword matching.
This improves retrieval accuracy because some questions require meaning-based search while others require exact keyword matching.
---
## Reranking
Reranking improves the order of retrieved results.
In this project, reranking can prioritize chunks with stronger term overlap or higher relevance to the user question.
---
## Streamlit
Streamlit is used to build the user interface for the assistant.
The Streamlit app provides an Arabic user interface where users can ask questions and see answers from the RAG engine.
The interface includes:
- SDAIA branding.
- Arabic RTL layout.
- Assistant title.
- Team names.
- Trainer name.
- Question input area.
- Answer panel.
- Data sources section.
- Robot-style assistant visual.
---
## Assistant Behavior
The assistant should answer only when relevant knowledge exists in the indexed sources.
If the question is unrelated or not covered by the available data, the assistant should say:
"لم أجد إجابة مرتبطة بهذا السؤال في مصادر البيانات المتاحة."
This behavior prevents hallucination and keeps the assistant grounded.
---
## Example Questions
The assistant should be able to answer questions such as:
- ما هي طبقات Lakehouse في هذا المشروع؟
- ما الفرق بين Bronze و Silver و Gold؟
- ما هي مصادر البيانات المستخدمة؟
- ما دور Kafka في المشروع؟
- لماذا Kafka اختياري؟
- ما دور Docker؟
- كيف يتم فحص جودة البيانات؟
- ما معنى SLA؟
- ما دور RAG في المشروع؟
- ما وظيفة Streamlit في المشروع؟
- ما دور Airflow؟
- ما فائدة Great Expectations؟
- ما هو KPI Catalog؟
- كيف يدعم المشروع قطاع النقل والخدمات اللوجستية؟
---
## Example Answer: Lakehouse Layers
The Lakehouse architecture in this project follows the Medallion pattern with Bronze, Silver, and Gold layers.
Bronze stores raw data from logistics sources.
Silver cleans, validates, standardizes, and deduplicates the data.
Gold prepares business-ready KPI and SLA datasets for analytics, dashboards, and the AI assistant.
---
## Example Answer: Kafka Role
Kafka is an optional streaming ingestion layer in the project.
It can simulate real-time logistics events such as shipment updates, rail trips, or port operations.
The core project can still run without Kafka using generated batch data.
This makes the project easier to run while still showing that the architecture supports real-time ingestion.
---
## Example Answer: Docker Role
Docker is used to run supporting services in containers.
It can be used to run Kafka or other services without manually installing them on the machine.
Docker helps make the environment reproducible and easier to deploy.
---
## Example Answer: Data Quality
Data quality is checked using validation rules and Great Expectations.
The project checks missing values, duplicates, invalid types, required columns, value ranges, and schema consistency.
These checks help ensure that the data used by the assistant and analytics layers is reliable.
---
## Example Answer: SLA
SLA means Service Level Agreement.
In this project, SLA is used to measure whether logistics services meet expected time or quality thresholds.
Examples include shipment delay, incident response time, port handling time, rail delay, and data refresh timeliness.
---
## Project Execution Flow
The project execution flow is:
1. Generate synthetic transport and logistics data.
2. Validate data schemas.
3. Load raw data into Bronze.
4. Clean and standardize data into Silver.
5. Create curated Gold tables.
6. Run data quality checks.
7. Build the RAG index.
8. Run the Streamlit assistant interface.
9. Ask questions using the assistant.
---
## Enterprise Production Simulation
The project simulates an enterprise production environment by including:
- Modular folder structure.
- Data ingestion.
- Schema validation.
- Lakehouse pipeline.
- Data quality checks.
- Optional Kafka streaming.
- Airflow orchestration.
- OpenLineage events.
- RAG pipeline.
- Streamlit interface.
- README documentation.
- Rubric coverage evidence.
---
## Optional Cloud Data Warehouse Layer
The project can integrate with a cloud data warehouse as an optional serving layer.
Possible platforms include:
- Snowflake.
- Google BigQuery.
- Amazon Redshift.
- Azure Synapse Analytics.
- Microsoft Fabric.
- Databricks SQL.
These platforms can be used to serve curated Gold datasets to dashboards, BI tools, or AI applications.
In this project, the cloud data warehouse is optional because the main architecture is based on a Lakehouse pattern.
---
## Difference Between Snowflake and Lakehouse
Snowflake is a cloud data warehouse platform used for SQL analytics, BI, and data sharing.
A Lakehouse combines data lake flexibility with data warehouse reliability.
In this project, the main design is a Lakehouse architecture. Snowflake can be added as an optional serving layer for enterprise analytics.
---
## Final Summary
This project demonstrates an integrated AI data platform for the transport and logistics sector.
It combines data engineering, Lakehouse architecture, schema validation, data quality, optional streaming, orchestration, lineage, RAG, and a Streamlit-based AI assistant.
The assistant is grounded in indexed project knowledge and should only answer based on available sources.



## وصف البيانات
البيانات المستخدمة في هذا المشروع هي بيانات تجريبية مولّدة لمحاكاة قطاع النقل والخدمات اللوجستية. تم تصميم هذه البيانات لدعم بناء Lakehouse، فحص جودة البيانات، حساب المؤشرات، ومساعدة نموذج RAG في الإجابة على الأسئلة المتعلقة بالبيانات.
## مصادر البيانات المتولدة
تشمل البيانات المتولدة المصادر التالية:
1. بيانات الشحنات.
2. بيانات عمليات الموانئ.
3. بيانات رحلات السكك الحديدية.
4. بيانات حوادث الطرق.
5. بيانات الركاب.
6. كتالوج مؤشرات الأداء.
7. قوالب اتفاقيات مستوى الخدمة SLA.
---
## بيانات الشحنات
بيانات الشحنات تمثل حركة الشحن في قطاع النقل والخدمات اللوجستية.
تستخدم هذه البيانات لتحليل:
- عدد الشحنات.
- حالة الشحنة.
- وسيلة النقل المستخدمة.
- زمن التسليم.
- التأخير في التسليم.
- الالتزام بمستهدفات الخدمة.
- الأداء التشغيلي للشحنات.
أمثلة على الأسئلة التي يمكن الإجابة عليها من بيانات الشحنات:
- ما هي بيانات الشحنات الموجودة؟
- كيف يمكن تحليل أداء الشحنات؟
- ما علاقة بيانات الشحنات بمؤشرات SLA؟
- كيف يتم قياس التأخير في الشحنات؟
---
## بيانات عمليات الموانئ
بيانات الموانئ تمثل العمليات التشغيلية داخل الموانئ.
تستخدم هذه البيانات لتحليل:
- حركة المناولة.
- زمن معالجة العمليات.
- أداء الموانئ.
- كفاءة العمليات اللوجستية.
- مؤشرات التأخير أو الازدحام.
- الالتزام بمستويات الخدمة التشغيلية.
أمثلة على الأسئلة:
- ما دور بيانات الموانئ في المشروع؟
- كيف تساعد بيانات الموانئ في قياس الأداء؟
- ما المؤشرات الممكن استخراجها من عمليات الموانئ؟
---
## بيانات رحلات السكك الحديدية
بيانات السكك الحديدية تمثل الرحلات وحركة القطارات.
تستخدم هذه البيانات لتحليل:
- عدد الرحلات.
- الالتزام بالوقت.
- التأخير في الرحلات.
- أداء النقل بالسكك الحديدية.
- مؤشرات الاعتمادية والتشغيل.
أمثلة على الأسئلة:
- كيف يتم تحليل أداء رحلات السكك الحديدية؟
- ما المؤشرات المرتبطة بتأخير الرحلات؟
- كيف تدخل بيانات السكك في طبقة Gold؟
---
## بيانات حوادث الطرق
بيانات حوادث الطرق تمثل الحوادث أو البلاغات المرتبطة بشبكة الطرق.
تستخدم هذه البيانات لتحليل:
- عدد الحوادث.
- مواقع الحوادث.
- نوع الحادث.
- مستوى الخطورة.
- زمن الاستجابة.
- أثر الحوادث على الخدمات اللوجستية.
أمثلة على الأسئلة:
- ما دور بيانات حوادث الطرق؟
- كيف يتم استخدام بيانات الحوادث في جودة الخدمات؟
- كيف يمكن قياس زمن الاستجابة للحوادث؟
---
## بيانات الركاب
بيانات الركاب تمثل حركة الركاب واستخدام خدمات النقل.
تستخدم هذه البيانات لتحليل:
- عدد الركاب.
- توزيع الركاب حسب وسيلة النقل.
- مؤشرات الطلب على خدمات النقل.
- الاتجاهات التشغيلية.
- دعم قرارات التخطيط والتحسين.
أمثلة على الأسئلة:
- ما هي بيانات الركاب؟
- كيف تساعد بيانات الركاب في تحليل قطاع النقل؟
- ما المؤشرات الممكن استخراجها من بيانات الركاب؟
---
## كتالوج مؤشرات الأداء
كتالوج مؤشرات الأداء يحتوي على تعريفات المؤشرات المستخدمة في المشروع.
يساعد الكتالوج في توحيد فهم المؤشرات وربطها بمصادر البيانات.
أمثلة على المؤشرات:
- إجمالي عدد الشحنات.
- نسبة التسليم في الوقت المحدد.
- متوسط التأخير.
- عدد الرحلات.
- معدل الالتزام بالـ SLA.
- عدد الحوادث.
- حجم الركاب.
- مؤشرات جودة البيانات.
أمثلة على الأسئلة:
- ما هو كتالوج المؤشرات؟
- ما المؤشرات المستخدمة في المشروع؟
- كيف ترتبط المؤشرات بمصادر البيانات؟
---
## قوالب SLA
قوالب SLA تمثل اتفاقيات مستوى الخدمة المستخدمة لمقارنة الأداء الفعلي بالمستهدف.
تستخدم SLA لقياس:
- زمن معالجة الشحنات.
- زمن تأخير الرحلات.
- زمن الاستجابة للحوادث.
- زمن تشغيل أو معالجة عمليات الموانئ.
- التزام الخدمات بالمستويات المستهدفة.
أمثلة على الأسئلة:
- ما معنى SLA في المشروع؟
- كيف يتم قياس الالتزام بالـ SLA؟
- ما علاقة SLA ببيانات الشحنات والرحلات والحوادث؟
---
## علاقة البيانات بطبقات Lakehouse
تمر البيانات المتولدة عبر ثلاث طبقات رئيسية:
### Bronze Layer
تخزن البيانات الخام كما تم توليدها أو استقبالها.
تشمل بيانات Bronze:
- بيانات الشحنات الخام.
- بيانات الموانئ الخام.
- بيانات السكك الحديدية الخام.
- بيانات حوادث الطرق الخام.
- بيانات الركاب الخام.
### Silver Layer
تنظف البيانات وتوحدها.
تشمل المعالجة في Silver:
- إزالة التكرارات.
- معالجة القيم المفقودة.
- توحيد أسماء الحقول.
- تصحيح أنواع البيانات.
- التحقق من صحة القيم.
- تجهيز البيانات للاستخدام التحليلي.
### Gold Layer
تجهز البيانات النهائية للتحليل.
تشمل مخرجات Gold:
- جداول مؤشرات الأداء.
- ملخصات SLA.
- مؤشرات جودة البيانات.
- بيانات جاهزة للداشبورد.
- بيانات يمكن استخدامها في المساعد الذكي.
---
## جودة البيانات
يتم فحص جودة البيانات المتولدة للتأكد من صلاحيتها للتحليل.
تشمل فحوصات الجودة:
- التحقق من وجود الأعمدة المطلوبة.
- فحص القيم المفقودة.
- فحص التكرارات.
- التحقق من أنواع البيانات.
- التحقق من القيم غير المنطقية.
- التأكد من توافق البيانات مع المخطط Schema.
أمثلة على الأسئلة:
- كيف يتم فحص جودة البيانات؟
- ما أنواع مشاكل جودة البيانات؟
- لماذا جودة البيانات مهمة في المشروع؟
---
## استخدام البيانات في RAG
يستخدم المساعد الذكي هذه المعرفة لفهم البيانات المتولدة والإجابة على الأسئلة المتعلقة بها.
المساعد لا يفترض إجابة من خارج المصادر المتاحة.
إذا كان السؤال غير موجود أو غير مدعوم بالمعلومات المتوفرة، يجب أن يجيب:
لم أجد إجابة مرتبطة بهذا السؤال في مصادر البيانات المتاحة.
---
## أمثلة أسئلة مناسبة للمساعد
- ما هي مصادر البيانات المتولدة؟
- ما هي بيانات الشحنات؟
- ما دور بيانات الموانئ؟
- كيف تستخدم بيانات السكك الحديدية؟
- ما فائدة بيانات حوادث الطرق؟
- ما المقصود ببيانات الركاب؟
- ما هو كتالوج مؤشرات الأداء؟
- ما هي قوالب SLA؟
- كيف تمر البيانات عبر Bronze و Silver و Gold؟
- كيف يتم فحص جودة البيانات؟
- كيف ترتبط البيانات بالمساعد الذكي؟
- ما البيانات المستخدمة لحساب مؤشرات الأداء؟
