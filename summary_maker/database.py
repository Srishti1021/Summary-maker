import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

#User Table
class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(64))
    group = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f'{self.id}|{self.name}|{self.group}'
    
class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"))
    contact = Column(String(50), default='9234567890')
    gender = Column(String(50), default='Male')
    dob = Column(String(50), default='01/01/2000')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return self.id

class File(Base):
    __tablename__ = 'files'
    uid = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)
    filename = Column(String(50))
    file_path = Column(String(50))
    file_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


    
if __name__ == '__main__':
    # for running file
    engine = create_engine('sqlite:///database.sqlite')
    Base.metadata.create_all(engine)