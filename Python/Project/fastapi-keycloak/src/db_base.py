from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

_Base = declarative_base(metadata=MetaData(schema='datasets'))