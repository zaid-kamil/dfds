from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime,default=datetime.now)
class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    user = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime,default=datetime.now)

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    result = Column(Boolean)
    score = Column(Float)
    created_at = Column(DateTime,default=datetime.now)

def get_db():
    engine = create_engine('sqlite:///deepfake.db')
    return sessionmaker(bind=engine)()

def save_to_db(object):
    db = get_db()      # open database
    db.add(object)     # insert object
    db.commit()        # save changes
    db.close()         # close database

def get_all(object):
    db = get_db()
    result = db.query(object).all()
    db.close()
    return result

def get_by_id(object, id):
    db = get_db()
    result = db.query(object).get(id)
    db.close()
    return result

#create database
if __name__ == "__main__":
    engine = create_engine('sqlite:///deepfake.db')
    Base.metadata.create_all(engine)