from sqlalchemy import Column, Integer, String, DateTime, Double
from db import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, autoincrement=True, primary_key=True)
    transaction_date = Column(DateTime)
    customer_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    amount = Column(Double, nullable=False, default=0)