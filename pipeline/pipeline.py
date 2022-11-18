import os
from uuid import uuid4
from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Custom Airflow Contrib Import
from airflow_contrib_v1_0_47.config.yaml_config import load_config
from airflow_contrib_v1_0_47.util.preconditions import check_primitive_and_initialized as verify
from airflow_contrib_v1_0_47.operators.utility_operators import (
    VariableBroadcastOperator,
    DagRunStatusOperator
)
from airflow_contrib_v1_0_47.operators.emr_create_stack import EmrCreateStackSyncOperator
from airflow_contrib_v1_0_47.operators.emr_terminate_stack import EmrTerminateStackOperator

pipeline_dir = os.path.dirname(os.path.realpath(__file__))

config = load_config(pipeline_dir, 'config.yaml').base

dag_config = config.airflow_config.dag
emr_config = config.emr_config
connections = config.connections

region = verify(connections.aws.region, 'region')

# Verify required default dag arguments
for key in ['queue', 'start_date', 'retries', 'retry_delay']:
    verify(dag_config.default_args.get(key), key)

dag = DAG(
    dag_id=verify(dag_config.id, 'dag_id'),
    schedule_interval=verify(dag_config.schedule_interval, 'schedule_interval'),
    max_active_runs=verify(dag_config.max_active_runs, 'max_active_runs'),
    concurrency=verify(dag_config.concurrency, 'concurrency'),
    catchup=verify(dag_config.catchup, 'catchup'),
    default_args=dag_config.default_args.to_dict()
)

variables_broadcast = VariableBroadcastOperator(
    task_id='variables_broadcast',
    templates_dict=config.xcom_variables.to_dict(),
    dag=dag
)

create_emr_stack = EmrCreateStackSyncOperator(
    task_id='create_emr_stack_sync',
    region=region,
    account=verify(connections.aws.account, 'aws_account'),
    stack_name=verify(emr_config.base_stack_name, 'base_stack_name'),
    resource_tags=emr_config.resource_tags.to_dict(),
    job_flow_overrides=emr_config.job_flow_overrides.to_dict(),
    alarm_topic_name=emr_config.alarm.topic,
    emr_idle_min_minutes=emr_config.alarm.idle_timeout,
    dag=dag
)

stack_name = '{{ ti.xcom_pull(task_ids="create_emr_stack_sync", key="stack_name") }}'
job_flow_id = '{{ ti.xcom_pull(task_ids="create_emr_stack_sync", key="job_flow_id") }}'

# For adding EMR steps for your job, see:
# https://github.com/integralads/ds-platform-airflow-contrib/blob/master/airflow_contrib/operators/emr_add_steps.py
# https://github.com/integralads/ds-platform-airflow-contrib/blob/master/airflow_contrib/operators/emr_step_builder_operators.py

delete_emr_stack = EmrTerminateStackOperator(
    task_id='terminate_emr_stack',
    region=region,
    stack_name=stack_name,
    dag=dag
)

dag_run_status = DagRunStatusOperator(
    task_id='dag_run_status',
    retries=0,
    dag=dag
)

variables_broadcast >> create_emr_stack >> delete_emr_stack >> dag_run_status
