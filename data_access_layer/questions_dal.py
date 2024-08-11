import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from data_access_layer.categories_dal import store_categories, fix_categories_names

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))
database = client['questions']
collection = database['questions']

def store_questions_and_categories(questions, categories):
    collection.insert_many(questions)
    store_categories(categories=categories)

def store_opentdb_questions(questions):
    collection.insert_many(questions)
    fix_categories_names(local_collection=collection)
    fix_questions()

def fix_questions():
    replacements = {
        '&quot;': '"',
        '&#039;': "'",
        '&amp;': '&',
        '&ldquo;': '"',
        '&rdquo;': '"',
        '&eacute;': 'e',
        '&ecirc;': 'e',
        '&uuml;': 'u',
        '&sup2;': '^2',
        '&Uuml;': 'U',
        '&deg;': '',
        '&rsquo;': "'",
        '&minus;': '-',
        '&hellip;"': '...',
        '&lsquo;': "'",
        '&ndash;': '-',
        '&ouml;': 'o',
        '&Aring;': 'A',
        '&micro;': 'mu',
        '&Eacute;': 'E',
        '&aacute;': 'a',
        '&shy;': '',
        '&pi;': 'pi',
        '&uacute;': 'u',
        '&ocirc;': 'o'
    }

    documents_to_update = collection.find({'question': {'$regex': '|'.join(replacements.keys())}})

    for document in documents_to_update:
        corrected_question = document['question']
        for entity, replacement in replacements.items():
            corrected_question = corrected_question.replace(entity, replacement)
        collection.update_one({'_id': document['_id']}, {'$set': {'question': corrected_question}})

def get_random_question():
    random_question = collection.aggregate([{'$sample': {'size': 1}}])
    random_question = list(random_question)[0]
    del random_question['_id']
    return random_question

def get_questions_by_filter(type: str = None, category: str = None, difficulty: str = None):
    query = {}

    if type:
        query['type'] = type.lower()
    if category:
        query['category'] = category.title().replace('And', 'and')
    if difficulty:
        query['difficulty'] = difficulty.lower()

    db_questions = collection.find(query, {'_id': 0})
    questions = [question for question in db_questions]
    questions_length = len(questions)

    if questions_length > 50:
        questions = random.sample(questions, 50)

    return questions, questions_length
