from http.client import HTTPException
from airflow import DAG
from airflow.sdk import Variable, task
from sqlalchemy.orm import Session
from include.models import Base, engine
from dataset import dataset

import requests

def map_table_model(table_name: str):
    return {m.tables[0].name: m.class_ for m in Base.registry.mappers}[table_name]

with DAG(
    dag_id='insert_data_dag',
    schedule='@daily'
) as dag:
    @task
    def login(ti=None):
        response = requests.post(f'{Variable.get('API_URL')}/login', json={
            'username': Variable.get('API_USERNAME'),
            'password': Variable.get('API_PASSWORD')
        })

        if response.status_code != 200:
            raise HTTPException(f'{response.status_code}\n{response.content}')

        return response.json()

    @task
    def retrieve_endpoints():
        return ['games', 'teams']
    
    @task
    def retrieve_data(endpoint: str, token: str, ds: str):
        return (endpoint, requests.get(f'{Variable.get('API_URL')}/{endpoint}', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'date': ds
        }).json())
    
    @task(outlets=[dataset])
    def insert_data(data):
        table, values = data

        with Session(engine) as session:
            records = [map_table_model(table)(**obj) for obj in values]
            [session.merge(record) for record in records]
            session.commit()
    
    insert_data.expand(data=retrieve_data.partial(token=login()).expand(endpoint=retrieve_endpoints()))