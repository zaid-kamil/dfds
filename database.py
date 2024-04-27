from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from datetime import datetime

Base = declarative_base()
class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    created_at = Column(DateTime,default=datetime.now)


def get_db():
    engine = create_engine('sqlite:///deepfake.db')
    return sessionmaker(bind=engine)()

def save_to_db(object):
    db = get_db()      # open database
    db.add(object)     # insert object
    db.commit()        # save changes
    db.close()         # close database

#create database
if __name__ == "__main__":
    engine = create_engine('sqlite:///deepfake.db')
    Base.metadata.create_all(engine)