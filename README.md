![image](https://user-images.githubusercontent.com/75282285/222922597-5cc59d8c-96b9-4ba2-b54b-2454f7c26f08.png)


# Python_Airflow_Snowflake_Trigger
I used Airflow to build the DAGs to query Snowflake. If the table have new rows, it will trigger the DAG to send mail. 

# Project Goal
* Use the lib to connect Snowflake in Airflow. 
* Can set the schedule interval in Airflow.
* Can read and set varable in Airflow.
* Can use SnowflakeHook to query data in Airflow.
* Can use xcom to get the result of other function in Airflow.
* can judge and trggir another DAG. and can set the schedule interval. 
* Can send mail with Airflake.

# Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Steps](#project_steps)
3. [Troubleshooting](#troubleshooting)
4. [Reference](#reference)

# Prerequisites  <a name="prerequisites"></a>
- Ubuntu 20.04 OS
- Airflow 2.5
- Snowflake

# Main code
```
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
    description=f"zsb! A good man!",
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
    task3 = PythonOperator(
        task_id='task_pass',
        python_callable=some_other_function,
    )
    count_query >> store_val_to_airflow >> branch_task >> [trigger_next_dag, task3]
```

# project_steps <a name="project_steps"></a>
## Build Airflow test env
![image](https://user-images.githubusercontent.com/75282285/208811379-6ba7e2de-9ece-413e-a993-1f9d40091af7.png)


## DAGs
There are two DAGs, one named `a_zsb_monitor`, the ohter named `a_zsb_send_mail`. The  `a_zsb_monitor` used to monitor the table named `zsb_tb` of Snowflake, and `a_zsb_send_mail` used to be trigger to send mail if the table has new rows.
![image](https://user-images.githubusercontent.com/75282285/208808318-43a7f891-8a73-4857-af0e-702fa4d4a6db.png)

## The Graph in AirFlow
From the Graph, you will see it judge and BranchPythonOperator. 
![image](https://user-images.githubusercontent.com/75282285/208809076-40075b18-75c8-4c7f-a869-bc9e1352a974.png)

## The Grid in Airflow Control panel
It runs every 2 mins. If it find the zsb_tb table has new row, will run the my_trigger and send mail to me, otherwise, it do nothing.
![image](https://user-images.githubusercontent.com/75282285/208809854-8052d05c-07e1-4b20-8b04-7c6f2d9aa35e.png)


## The detail of the 'a_zsb_monitor' DAG
![image](https://user-images.githubusercontent.com/75282285/208809500-49646905-acd3-497f-846f-00c872a0c44b.png)


## The Variable
This variable named snowflake_count_number store the rows number of table zsb_tb of Snowflake. If DAG find the new rows in Snowflake, this variable will be updated to the newest rows number.
![image](https://user-images.githubusercontent.com/75282285/208809988-df17a77b-4544-42d5-acf8-12b1c91bac41.png)

## The connection
For secure to store the connection parameters of Snowflake, I add the connection in Airflow. 
![image](https://user-images.githubusercontent.com/75282285/208810345-a903aae9-09a4-41ed-94e5-80104b5ea141.png)
It includes some items, such as Loginm, password, Account, Warehouse, Database etc.
![image](https://user-images.githubusercontent.com/75282285/208811501-ed40cd71-b531-44b3-8a6c-0760885aa5f6.png)


## The schedule
It will monitor every 2 mins.
![image](https://user-images.githubusercontent.com/75282285/208811802-297ede0b-0c15-461b-80ff-8ad36fee3bc7.png)

# Troubleshooting <a name="troubleshooting"></a>
## Issue1: Can't open the login page
You want to run Airflow in the background. After you run the `airflow webserver --port 8080 -D`, but you will find you can't open the `xxxx:8080` to login.      
Solution: Delelet all *.pid files in the /home/zsb/airflow/, run the command `airflow webserver --port 8080 -D` again. It will be OK.
![image](https://user-images.githubusercontent.com/75282285/208895730-9c2178f0-5861-45f5-8ade-534e2e4ff431.png)

## Issue2: Configure the connection of Snowflake in Airflow
In the parameters in the page of connection of Snowflake, the Host item is useless.You can test it is OK in connection page even if you don't input Host address in Airflow.     
If you use BaseHook.get_connection, you will find only `login`, `password`, `schema` are useful, other items can't be pulled in BaseHook.get_connection.

# <a name="reference">Reference</a>
[Basic Concepts](https://airflow.apache.org/docs/apache-airflow/1.10.6/concepts.html?highlight=branch%20operator)</br>
[Set up a Database](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html)</br>
[Providers packages](https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html)</br>
[S3 example](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_modules/tests/system/providers/amazon/aws/example_s3.html)</br>
[Snowflake example](https://community.snowflake.com/s/article/How-to-connect-Apache-Airflow-to-Snowflake-and-schedule-queries-jobs)</br>

