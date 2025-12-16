from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

DAG_ID = "youtube_etl_by_year"

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "retries": 1
}

with DAG(
    dag_id=DAG_ID,
    description="ETL de YouTube - Todas las tecnologías por año secuencial",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@weekly",  # Ejecutar semanalmente
    catchup=False,
    tags=["youtube", "etl", "postgres", "year-control"]
) as dag:

    # Una sola tarea que procesa todas las tecnologías del próximo año pendiente
    run_etl_all_technologies = BashOperator(
        task_id="run_etl_all_technologies",
        bash_command="python /opt/airflow/scripts/run_etl.py"
    )
