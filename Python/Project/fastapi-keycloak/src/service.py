from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, select, text
from sqlalchemy.sql.sqltypes import String
from db import engine, Base
from models import *
import pandas as pd
import io

def map_table_model(table_name: str):
    return {m.tables[0].name: m.class_ for m in Base.registry.mappers}[table_name]

def get_datasets():
    with Session(engine) as session:
        lst = [dataset for dataset in session.execute(text(
            '''
            SELECT * 
            FROM pg_tables WHERE schemaname = \'datasets\'
            ''')).fetchmany()[0] if isinstance(dataset, str) and dataset not in ['datasets', 'postgres']]
        
        return lst
    
def search_keywords(dataset: str, keywords: List[str]):
    with Session(engine) as session:
        table_class = map_table_model(dataset)
        fields = [field for field in vars(table_class).keys() 
                    if not field.startswith('_') and isinstance(vars(table_class).get(field).type, String)]

        return session.query(table_class).filter(
            or_(*[getattr(table_class, field).ilike(keyword) for keyword in keywords for field in fields])
        ).all()
    
def export_csv(dataset: str):
    with Session(engine) as session:
        stream = io.StringIO()
        df = pd.read_sql(session.query(map_table_model(dataset)).statement, session.bind)
        df.to_csv(stream, index=False)
        
        return stream