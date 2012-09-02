# DB.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Text, Integer, Boolean

engine = create_engine('sqlite:///spidersilk.db')
session = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base(bind=engine)

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True,nullable=False)
	name = Column(String, nullable=False)
	gender = Column(String)
	bio = Column(Text)
	species = Column(String)
	password = Column(String, nullable=False)
	minorflag = Column(Boolean)
	accepttos = Column(Boolean)
	
	def __init__ (self, name, species, password):
		self.name = name
		self.species = species
		self.password = password

	def __repr__(self):
		return "<User(%s)>" % (self.name)

def addDefault():
	defaultUser = User('admin','admin','admin')
	session.add(defaultUser)
	session.commit()


