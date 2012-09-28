# DB.py

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Text, Integer, Boolean

#engine = create_engine('sqlite:///spidersilk.db')
engine = create_engine('postgresql:///spidersilk')

session = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base(bind=engine)

class User(Base):
	""" Default User Class Model """
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True,nullable=False)
	name = Column(String, nullable=False)
	gender = Column(String)
	bio = Column(Text)
	species = Column(String)
	password = Column(String, nullable=False)
	minorflag = Column(Boolean)
	accepttos = Column(Boolean)
	stories = relationship("Story", backref="users")

	def __init__ (self, name, species, password):
		self.name = name
		self.species = species
		self.password = password

	def __repr__(self):
		return "<User(%s)>" % (self.name)

class Story(Base):
	""" Story Class Model """
	__tablename__ = 'stories'
	id = Column(Integer, primary_key=True, nullable=False)
	uid = Column(Integer, ForeignKey('users.id'))
	title = Column(String, nullable=False)
	text = Column(Text)
	adult = Column(Boolean)

	def __init__(self, title):
		self.title = title
		
	def __repr__(self):
		return "<Story(%s)>" % (self.title)

def addDefault():
	""" Add admin with user / pass of admin """
	defaultUser = User('admin','admin','$2a$12$AHg0z21DK3EX6PxvhURE0urYEgUbYO/VGdD9mRN/XFr372eM6kpYS')
	session.add(defaultUser)
	session.commit()

def init_db():
	""" Initialize the database with no users """
	Base.metadata.create_all(bind=engine)
	print "Database Initialized"
	
def drop_db():
	""" Delete the database """
	Base.metadata.drop_all(bind=engine)
	print "Database Dropped"

def refresh_db():
	""" Refresh the database """
	drop_db()
	init_db()
	print "Database Refreshed"


