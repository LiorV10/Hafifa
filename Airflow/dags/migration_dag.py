from datetime import datetime

from airflow.models import DAG
from airflow.models.param import Param
from airflow.sdk import Variable

from airflow_provider_alembic.operators.alembic import AlembicOperator
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
        "migration_dag",
        schedule="@once",
        params={
            "command": Param("upgrade"),
            "revision": Param("head")
        }
) as migration_dag:
    migration_start = BashOperator(
        task_id="migration_start",
        bash_command='cd /usr/local/airflow/dags/migration && alembic revision --autogenerate -m ""'
    )
    
    upgrade = AlembicOperator(
        task_id="migration",
        conn_id='postgres',
        command="{{ params.command }}",
        revision="{{ params.revision }}",
        script_location="/usr/local/airflow/dags/migration",
    )

    migration_start >> upgrade