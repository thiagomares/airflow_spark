from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.dummy import DummyOperator
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from datetime import datetime
import pyarrow.parquet as pq
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 18),
    'retries': 1,
}

# Função para inserir dados no Druid
def inserir_dados_no_druid():
    # Caminho do arquivo Parquet
    parquet_file = '/home/thiagomares/Área de trabalho/fluxos_de_trabalho/include/dados.parquet'
    
    # Leitura do arquivo Parquet usando Pandas ou PyArrow
    df = pd.read_parquet(parquet_file)
    
    # Conversão para JSON ou outro formato suportado pelo Druid
    data_json = df.to_json(orient='records')
    
    # Aqui você faria a chamada à API do Druid ou utilizaria uma ferramenta como requests
    # para enviar os dados ao Druid.
    # Exemplo usando requests (ajuste conforme necessário):
    # import requests
    # url = "http://druid-coordinator-endpoint/druid/indexer/v1/task"
    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url, headers=headers, data=data_json)
    
    # Imprimir os dados para depuração
    print(data_json)

with DAG(
    dag_id='spark_test_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    dummy1 = DummyOperator(
        task_id='Início'
    )

    spark_job = SparkSubmitOperator(
        task_id='run_spark_job',
        application='./include/teste.py',
        name='spark_test_job',
        conn_id='spark_default',
        verbose=1,
    )

    # Operador Python para inserir os dados no Druid
    insere_dados = PythonOperator(
        task_id='insere_dados_no_druid',
        python_callable=inserir_dados_no_druid
    )

    dummy2 = DummyOperator(
        task_id = 'Fim'
    )

    # Definindo a sequência das tarefas
    dummy1 >> spark_job >> insere_dados >> dummy2
