from sqlalchemy import Column, Text, Integer
from .db import Base

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, autoincrement=True)
	password = Column(Text, nullable=False)
	email = Column(Text, nullable=False)