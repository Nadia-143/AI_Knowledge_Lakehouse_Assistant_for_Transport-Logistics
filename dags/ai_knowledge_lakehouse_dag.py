from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
PROJECT_DIR='/opt/airflow/dags/../'
with DAG(dag_id='ai_knowledge_lakehouse_assistant',start_date=datetime(2025,1,1),schedule_interval='@daily',catchup=False,tags=['transport','lakehouse','rag']) as dag:
    generate_data=BashOperator(task_id='generate_synthetic_data',bash_command=f'cd {PROJECT_DIR} && python src/data/generate_synthetic_data.py')
    lakehouse=BashOperator(task_id='build_delta_lakehouse',bash_command=f'cd {PROJECT_DIR} && python src/lakehouse/delta_pipeline.py')
    quality_gate=BashOperator(task_id='run_quality_gate',bash_command=f'cd {PROJECT_DIR} && python src/quality/great_expectations_checks.py')
    build_rag=BashOperator(task_id='build_rag_index',bash_command=f'cd {PROJECT_DIR} && python src/rag/build_index.py')
    generate_data >> lakehouse >> quality_gate >> build_rag
