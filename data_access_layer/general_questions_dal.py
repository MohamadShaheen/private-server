import random

def get_questions(collection):
    db_questions = collection.find({}, {'_id': 0})
    questions = [question for question in db_questions]
    questions_length = len(questions)

    if questions_length > 50:
        questions = random.sample(questions, 50)

    return questions, questions_length

def get_random_question(collection):
    questions = get_questions(collection)
    question = random.choice(questions)
    return question

def get_questions_by_filter(collection, type: str = None, category: str = None, difficulty: str = None):
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

def get_questions_categories(database):
    collection = database['categories']
    db_categories = collection.find({}, {'_id': 0})
    categories = [category['category'] for category in db_categories]
    return categories
