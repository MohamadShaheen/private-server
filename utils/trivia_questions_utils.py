from datetime import datetime
from data_access_layer.trivia_questions_dal import store_questions_and_categories
import requests
import logging

logging.basicConfig(filename='logs/trivia_questions_utils.log', level=logging.INFO, force=True)

def get_and_store_questions_and_categories():
    questions_id = set()
    categories = set()
    questions_data = []
    for _ in range(200):
        response = requests.get('https://the-trivia-api.com/v2/questions?limit=50')
        if response.status_code == 200:
            data = response.json()
            for question in data:
                question_id = question['id']

                if question_id not in questions_id:
                    category = question['category'].replace('_', ' ').title().replace('And', 'and')
                    questions_id.add(question_id)
                    questions_data.append({
                        '_id': question_id,
                        'type': 'multiple',
                        'difficulty': question['difficulty'],
                        'category': category,
                        'question': question['question']['text'],
                        'correct_answer': question['correctAnswer'],
                        'incorrect_answers': question['incorrectAnswers']
                    })
                    categories.add(category)
        else:
            logging.error(f'Error: {response.status_code} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

    categories_list = [{'category': category} for category in categories]
    store_questions_and_categories(questions=questions_data, categories=categories_list)
    logging.info(f"{len(questions_data)} Questions and {len(categories_list)} Categories have been stored successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
