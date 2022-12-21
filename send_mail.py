from __future__ import annotations
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import yfinance as yf
from airflow.models import Variable
from airflow.operators.email import EmailOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator, SnowflakeCheckOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.hooks.base_hook import BaseHook
from airflow.sensors.bash import BashSensor
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id=f"a_zsb_send_mail",
    default_args={
        "depends_on_past": False,
        "email": ['songbin.zhang@gmail.com'],
        "email_on_failure": True,
        "email_on_retry": True,
        "retries": 1,
        "retry_delay": timedelta(minutes=30),
        "snowflake_conn_id": "a_zsb_snowflake"
    },
    description=f"zsb! A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["zsbdata"],
    max_active_runs=1,
) as dag:
    dag.doc_md = "111111"
    email_task = EmailOperator(
        task_id='send_email',
        to=['songbin.zhang@gmail.com','jessiehuang2018@gmail.com'],
        subject='Stock Price is download',
        html_content="""
        <h3>Email Test</h3>
        {{ ds_nodash }}<br/>{{ dag }}<br/>
        {{ conf }}<br/>
        {{ next_ds }}<br/>
        {{ yesterday_ds }}<br/>
        {{ tomorrow_ds }}<br/>
        {{ execution_date }}<br/>
        """,
    )
