from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv(override=True)

engine = create_engine(os.getenv('DB_URL'))
Base = declarative_base(metadata=MetaData(schema=os.getenv('DB_SCHEMA')))
Base.metadata.create_all(engine)