from pymongo import MongoClient
import os
from dotenv import load_dotenv
from data_access_layer import general_questions_dal

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))
database = client['quiz_questions']
collection = database['questions']

def store_questions_and_categories(questions, categories):
    collection.insert_many(questions)
    database['categories'].insert_many(categories)

def get_questions():
    return general_questions_dal.get_questions(collection)

def get_random_question():
    return general_questions_dal.get_random_question(collection)

def get_questions_by_filter(type: str = None, category: str = None, difficulty: str = None):
    return general_questions_dal.get_questions_by_filter(collection, type, category, difficulty)

def get_questions_categories():
    return general_questions_dal.get_questions_categories(database)
