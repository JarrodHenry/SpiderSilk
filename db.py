# DB.py

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.schema import Column, Table
from sqlalchemy.types import String, Text, Integer, Boolean, DateTime

#engine = create_engine('sqlite:///spidersilk.db')
engine = create_engine('postgresql:///spidersilk')

session = scoped_session(sessionmaker(bind=engine, autoflush=False))

Base = declarative_base(bind=engine)


favstory_table = Table('favorites', Base.metadata,
	Column('user_id', Integer, ForeignKey('users.id')),
	Column('story_id', Integer, ForeignKey('stories.id'))
)

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
	faves = relationship("Story", secondary='favorites')

	def __init__ (self, name, species, password):
		self.name = name
		self.species = species
		self.password = password

	def __repr__(self):
		return "<User(%s)>" % (self.name)


tagstory_association_table = Table('tagstory', Base.metadata,
	Column('tag_id', Integer, ForeignKey('tags.id')),
	Column('story_id', Integer, ForeignKey('stories.id'))
)



class Story(Base):
	""" Story Class Model """
	__tablename__ = 'stories'
	id = Column(Integer, primary_key=True, nullable=False)
	uid = Column(Integer, ForeignKey('users.id'))
	title = Column(String, nullable=False)
	text = Column(Text)
	adult = Column(Boolean)
	tags = relationship("Tag",
		secondary = tagstory_association_table,
		backref = 'stories')
	recs = relationship("Reccomendation")
	favedby = relationship("User", secondary='favorites')

	def __init__(self, title):
		self.title = title
		
	def __repr__(self):
		return "<Story(%s)>" % (self.title)


class Tag(Base):
	"""Tags Model"""
	__tablename__ = 'tags'
	id = Column(Integer, primary_key=True, nullable=False)
	tagname = Column(String, nullable=False)

	def __init__(self, tagname):
		self.tagname = tagname	

	def __repr__(self):
		return "<Tag(%s)>" % (self.tagname)

class Reccomendation(Base):
	"""Recommendation Model"""
	__tablename__= 'recs'
	id = Column(Integer, primary_key=True, nullable=False)
	sid = Column(Integer, ForeignKey('stories.id'))
	uid = Column(Integer, ForeignKey('users.id'))
	uname = Column(Text)
	date = Column(DateTime) 	
	comment = Column(Text)

	def __init__(self, comment):
		self.comment = comment
	
	def __repr__(self):
		return "<Rec(%s,%s)" % (self.sid, self.uid)


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


