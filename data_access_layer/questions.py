import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))
database = client['opentdb_questions']
collection = database['questions']

def store_questions(questions):
    if collection.count_documents({}) == len(questions):
        return
    collection.insert_many(questions)
    fix_categories_names(local_collection=collection)
    fix_questions()

def store_categories(categories):
    local_collection = database['categories']
    if local_collection.count_documents({}) == len(categories):
        return
    local_collection.insert_many(categories)
    fix_categories_names(local_collection=local_collection)

def fix_categories_names(local_collection):
    replacements = {
        '&amp;': '&',
        'Entertainment: ': '',
        'Science: ': '',
        '&': 'and',
    }

    documents_to_update = local_collection.find({'category': {'$regex': '|'.join(replacements.keys())}})

    for document in documents_to_update:
        corrected_category = document['category']
        for entity, replacement in replacements.items():
            corrected_category = corrected_category.replace(entity, replacement)
        local_collection.update_one({'_id': document['_id']}, {'$set': {'category': corrected_category}})

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
        '&uacute;': 'u'
    }

    documents_to_update = collection.find({'question': {'$regex': '|'.join(replacements.keys())}})

    for document in documents_to_update:
        corrected_question = document['question']
        for entity, replacement in replacements.items():
            corrected_question = corrected_question.replace(entity, replacement)
        collection.update_one({'_id': document['_id']}, {'$set': {'question': corrected_question}})

def get_questions():
    db_questions = collection.find({}, {'_id': 0})
    questions = [question for question in db_questions]
    return questions

def get_random_question():
    questions = get_questions()
    question = random.choice(questions)
    return question

def get_questions_by_filter(type: str = None, category: str = None, difficulty: str = None):
    args = {
        'type': '',
        'category': '',
        'difficulty': ''
    }

    if type:
        args['type'] = type.lower()
    if category:
        args['category'] = category.title()
    if difficulty:
        args['difficulty'] = difficulty.lower()

    db_questions = collection.find(args, {'_id': 0})
    questions = [question for question in db_questions]
    return questions

def get_questions_categories():
    local_collection = database['categories']
    db_categories = local_collection.find({}, {'_id': 0})
    categories = [category['category'] for category in db_categories]
    return categories
