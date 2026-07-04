generate:
	python src/data/generate_synthetic_data.py
lakehouse:
	python src/lakehouse/delta_pipeline.py
quality:
	python src/quality/great_expectations_checks.py
rag:
	python src/rag/build_index.py
app:
	streamlit run src/app/streamlit_app.py
api:
	uvicorn src.api.main:app --reload
test:
	pytest -q
