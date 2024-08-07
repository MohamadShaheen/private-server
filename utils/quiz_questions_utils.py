from pprint import pprint

from data_access_layer.quiz_questions_dal import store_questions_and_categories
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import logging

load_dotenv()

quiz_token = os.getenv('QUIZ_TOKEN')
url = 'https://quizapi.io/api/v1/questions'
params = {'limit': 20}
headers = {'X-Api-Key': quiz_token}
logging.basicConfig(filename='logs/quiz_questions_utils.log', level=logging.INFO, force=True)

def get_and_store_questions_and_categories():
    questions_id = set()
    categories = set()
    questions_data = []
    for _ in range(300):
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 or response.status_code == 403:
            data = response.json()
            for question in data:
                question_id = question['id']

                # Make sure the question wasn't inserted before
                if question_id not in questions_id and question['multiple_correct_answers'] == 'false':
                    questions_id.add(question_id)
                    true_key = ''
                    # Fetch the correct answer
                    for key, value in question['correct_answers'].items():
                        if value.lower() == 'true':
                            true_key = key
                            break
                    if true_key == '':
                        true_key = question['correct_answer']
                    else:
                        true_key = true_key.replace('_correct', '')
                    correct_answer = question['answers'][true_key]
                    # If the answer is True or False make sure to upper first letter to keep consistent manner
                    if correct_answer.lower() == 'true' or correct_answer.lower() == 'false':
                        correct_answer = correct_answer.capitalize()
                    # Delete the correct answer to avoid adding it to incorrect answers
                    del question['answers'][true_key]
                    incorrect_answers = []
                    # Fetch incorrect answers
                    for value in question['answers'].values():
                        if value:
                            if value.lower() == 'true' or value.lower() == 'false':
                                value = value.capitalize()
                            incorrect_answers.append(value)

                    # Set the proper type
                    type = 'multiple'
                    if (correct_answer == 'True' and incorrect_answers[0] == 'False') or \
                            (correct_answer == 'False' and incorrect_answers[0] == 'True'):
                        type = 'boolean'

                    category = question['category']
                    if category == '':
                        category = 'Uncategorized'
                    questions_data.append({
                        '_id': question_id,
                        'type': type,
                        'difficulty': question['difficulty'].lower(),
                        'category': category,
                        'question': question['question'],
                        'correct_answer': correct_answer,
                        'incorrect_answers': incorrect_answers
                    })
                    categories.add(category)
        else:
            logging.error(f'Error: {response.status_code} - {response.content} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

    categories_list = [{'category': category} for category in categories]
    store_questions_and_categories(questions=questions_data, categories=categories_list)
    logging.info(f"{len(questions_data)} Questions and {len(categories_list)} Categories have been stored successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
