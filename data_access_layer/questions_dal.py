import random
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))
database = client['questions']
collection = database['questions']

def store_categories(categories_collection, categories):
    db_categories = categories_collection.find({})
    db_categories_set = set()

    for category in db_categories:
        db_categories_set.add(category['category'])

    for category in categories:
        if category['category'] not in db_categories_set:
            categories_collection.insert_one(category)

def store_questions_and_categories(questions, categories):
    collection.insert_many(questions)
    store_categories(categories_collection=database['categories'], categories=categories)

def store_opentdb_questions(questions):
    collection.insert_many(questions)
    fix_categories_names(local_collection=collection)
    fix_questions()

def store_opentdb_categories(categories):
    store_categories(categories_collection=database['categories'], categories=categories)
    fix_categories_names(local_collection=database['categories'])

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

def get_questions():
    db_questions = collection.find({}, {'_id': 0})
    questions = [question for question in db_questions]
    questions_length = len(questions)

    if questions_length > 50:
        questions = random.sample(questions, 50)

    return questions, questions_length

def get_random_question():
    questions, _ = get_questions()
    question = random.choice(questions)
    return question

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

def get_questions_categories():
    collection = database['categories']
    db_categories = collection.find({}, {'_id': 0})
    categories = [category['category'] for category in db_categories]
    return categories
