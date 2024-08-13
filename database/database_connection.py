import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

mysql_url = os.getenv('MYSQL_URL')
mysql_database = os.getenv('MYSQL_DATABASE')
engine = create_engine(mysql_url)
connection = engine.connect()
connection.execute(text(f'CREATE DATABASE IF NOT EXISTS {mysql_database}'))
connection.close()
engine = create_engine(mysql_url + '/' + mysql_database)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
