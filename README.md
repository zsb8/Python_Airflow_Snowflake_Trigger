# Python_Airflow_Snowflake_Trigger
Use Airflow to query Snowflake. If the table have new rows, it will trigger the DAG to send mail. 

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

# project_steps <a name="project_steps"></a>

## DAGs
There are two DAGs, one named `a_zsb_monitor`, the ohter named `a_zsb_send_mail`. The  `a_zsb_monitor` used to monitor the table named `zsb_tb` of Snowflake, and `a_zsb_send_mail` used to be trigger to send mail if the table has new rows.
![image](https://user-images.githubusercontent.com/75282285/208808318-43a7f891-8a73-4857-af0e-702fa4d4a6db.png)

## The Grah in AirFlow

