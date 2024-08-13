import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))
database = client['questions']
collection = database['categories']

def store_categories(categories):
    db_categories = collection.find({})
    db_categories_set = set()

    for category in db_categories:
        db_categories_set.add(category['category'])

    for category in categories:
        if category['category'] not in db_categories_set:
            collection.insert_one(category)

def store_opentdb_categories(categories):
    store_categories(categories=categories)
    fix_categories_names(local_collection=database['categories'])

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

def get_questions_categories():
    db_categories = collection.find({}, {'_id': 0})
    categories = [category['category'] for category in db_categories]
    return categories
