from datetime import datetime
from data_access_layer.questions import store_questions, store_categories
from dotenv import load_dotenv
import requests
import logging
import os

load_dotenv()
opentdb_token = os.getenv('OPENTDB_TOKEN')
logging.basicConfig(filename='logs/utils_get_questions.log', level=logging.INFO)

def get_and_store_questions():
    while True:
        response = requests.get(f'https://opentdb.com/api.php?amount=50&token={opentdb_token}')
        if response.status_code == 200:
            if response.json()['response_code'] == 4:
                while True:
                    response = requests.get(f'https://opentdb.com/api.php?amount=48&token={opentdb_token}')
                    if response.status_code == 200:
                        store_questions(response.json()['results'])
                        return
            store_questions(response.json()['results'])
            logging.info(f"Questions have been stored successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
        else:
            logging.error(f'Error: {response.status_code}')

def get_and_store_categories():
    response = requests.get('https://opentdb.com/api_category.php')
    if response.status_code == 200:
        categories = response.json()['trivia_categories']
        for category in categories:
            category['_id'] = category['id']
            category['category'] = category['name']
            del category['id']
            del category['name']
        store_categories(categories)
        logging.info(f"Categories have been stored successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    else:
        logging.error(f'Error: {response.status_code}')
