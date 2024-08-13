import logging
import requests
from datetime import datetime
from mongodb_data_access_layer.questions_dal import store_opentdb_questions
from mongodb_data_access_layer.categories_dal import store_opentdb_categories

logging.basicConfig(filename='logs/opentdb_questions_utils.log', level=logging.INFO, force=True)

def get_and_store_questions():
    opentdb_token = 'EMPTY'
    questions_data = []
    try:
        while True:
            response = requests.get(f'https://opentdb.com/api.php?amount=50&token={opentdb_token}')
            if response.status_code == 200:
                data = response.json()
                # Fetch OpenTDB token
                if data['response_code'] == 3:
                    token_response = requests.get('https://opentdb.com/api_token.php?command=request')
                    if token_response.status_code == 200:
                        opentdb_token = token_response.json()['token']
                        logging.info(f'OpenTDB token was fetched successfully - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
                        continue
                    else:
                        logging.error(f'Failed to fetch OpenTDB token - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
                        exit(1)
                if data['response_code'] == 4:
                    break
                questions_data.extend(data['results'])
            else:
                # 429 is the code for too many requests, we will avoid it to avoid excessive load on log file
                if response.status_code != 429:
                    logging.error(f'Error: {response.status_code} - {response.content} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
    except Exception as e:
        logging.error(f'Unexpected error occurred - {e} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

    store_opentdb_questions(questions=questions_data)
    logging.info(f'{len(questions_data)} questions have been stored successfully - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')

def get_and_store_categories():
    response = requests.get('https://opentdb.com/api_category.php')
    if response.status_code == 200:
        categories = response.json()['trivia_categories']
        for category in categories:
            category['category'] = category['name']
            del category['id']
            del category['name']
        store_opentdb_categories(categories)
        logging.info(f"{len(categories)} categories have been stored successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    else:
        logging.error(f'Error: {response.status_code} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
