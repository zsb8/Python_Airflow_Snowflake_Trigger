from __future__ import annotations
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator, SnowflakeValueCheckOperator
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import BranchPythonOperator
hook_conn = BaseHook.get_connection("a_zsb_snowflake")


def snowflake_variables(**context):
    my_changed = False
    sf = int(Variable.get("snowflake_count_number"))
    new_sf = context['ti'].xcom_pull(task_ids='count_query')
    if new_sf > sf:
        Variable.set(key="snowflake_count_number", value=new_sf)
        my_changed = True
    return my_changed


def count1():
    dwh_hook = SnowflakeHook(snowflake_conn_id="a_zsb_snowflake")
    re = dwh_hook.get_first("select count(*) from zsb_tb")
    result = re[0]
    return result


def determine_next_task(**context):
    result = context['ti'].xcom_pull(task_ids='store_val')
    if result:
        return 'my_trigger'
    else:
        return 'task_pass'


def some_other_function():
    pass


with DAG(
    dag_id=f"a_zsb_monitor",
    default_args={
        "depends_on_past": False,
        "email": ['songbin.zhang@gmail.com'],
        "email_on_failure": True,
        "email_on_retry": True,
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    description=f"zsb! A simple tutorial DAG",
    schedule_interval=timedelta(minutes=2),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["zsbdata"],
    max_active_runs=1,
) as dag:
    dag.doc_md = "4"
    count_query = PythonOperator(task_id="count_query", python_callable=count1)
    store_val_to_airflow = PythonOperator(task_id="store_val", python_callable=snowflake_variables)
    trigger_next_dag = TriggerDagRunOperator(
        trigger_dag_id="send_email",
        task_id="my_trigger",
        execution_date="{{ds}}",
        wait_for_completion=False,
        reset_dag_run=True,
    )
    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=determine_next_task,
    )
    task_pass = PythonOperator(
        task_id='task_pass',
        python_callable=some_other_function,
    )
    count_query >> store_val_to_airflow >> branch_task >> [trigger_next_dag, task_pass]
