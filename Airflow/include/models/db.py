from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base

try:
    from airflow.sdk import Variable
    engine = create_engine(Variable.get('DB_CONNECTION'))
except:
    engine = create_engine('postgresql://postgres:postgres@172.17.0.1:5431/postgres')

Base = declarative_base(metadata=MetaData(schema='public'))
Base.metadata.create_all(engine)