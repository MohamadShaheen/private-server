import os
import random
from dotenv import load_dotenv
from pymongo import MongoClient
from mongodb_data_access_layer.categories_dal import store_categories, fix_categories_names

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URL'))
database = client['questions']
collection = database['questions']

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
    '&ocirc;': 'o',
    '&ntilde;': 'n',
    '&auml;': 'a',
    '&iacute;': 'i',
    '&lt;': '<',
    '&gt;': '>',
    '&Omicron;': 'O',
    '&oacute;': 'o',
    '&aring;': 'a',
    '&reg;': '',
    '&trade;': '',
    '&prime;': "'",
    '&Prime;': '"',
    '&atilde;': 'a',
    '&euml;': 'e',
    '&Delta;': 'Δ',
    '&Ouml;': 'O',
    '&Aacute;': 'A',
    '&lrm;': '',
    '&iuml;': 'i',
    '&Sigma;': 'Σ',
    '&Pi;': 'Π',
    '&Nu;': 'ν',
    '&egrave;': 'e',
    '&divide;': '÷'
}

def store_questions_and_categories(questions, categories):
    collection.insert_many(questions)
    store_categories(categories=categories)

def store_opentdb_questions(questions):
    collection.insert_many(questions)
    fix_categories_names(local_collection=collection)
    fix_questions()
    fix_correct_answers()
    fix_incorrect_answers()

def fix_questions():
    documents_to_update = collection.find({'question': {'$regex': '|'.join(replacements.keys())}})

    for document in documents_to_update:
        corrected_question = document['question']
        for entity, replacement in replacements.items():
            corrected_question = corrected_question.replace(entity, replacement)
        collection.update_one({'_id': document['_id']}, {'$set': {'question': corrected_question}})

def fix_correct_answers():
    documents_to_update = collection.find({'correct_answer': {'$regex': '|'.join(replacements.keys())}})

    for document in documents_to_update:
        corrected_answer = document['correct_answer']
        for entity, replacement in replacements.items():
            corrected_answer = corrected_answer.replace(entity, replacement)
        collection.update_one({'_id': document['_id']}, {'$set': {'correct_answer': corrected_answer}})

def fix_incorrect_answers():
    documents_to_update = collection.find({'incorrect_answers': {'$regex': '|'.join(replacements.keys())}})

    for document in documents_to_update:
        incorrect_answers = []
        for incorrect_answer in document['incorrect_answers']:
            for entity, replacement in replacements.items():
                incorrect_answer = incorrect_answer.replace(entity, replacement)
            incorrect_answers.append(incorrect_answer)
        collection.update_one({'_id': document['_id']}, {'$set': {'incorrect_answers': incorrect_answers}})

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
