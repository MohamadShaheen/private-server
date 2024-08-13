from sqlalchemy import Column, Integer, String
from database.database_connection import Base, engine


class Founder(Base):
    __tablename__ = 'founders'

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), unique=False, nullable=False)
    password = Column(String(100), unique=False, nullable=False)
    ultimate_founder_token = Column(String(100), unique=False, nullable=True)

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), unique=False, nullable=False)
    password = Column(String(50), unique=False, nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), unique=False, nullable=False)
    password = Column(String(50), unique=False, nullable=False)

# Base.metadata.create_all(bind=engine)
