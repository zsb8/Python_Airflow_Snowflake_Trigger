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


