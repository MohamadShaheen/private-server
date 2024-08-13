import os
import json
from utils import quiz_questions_utils
from utils import trivia_questions_utils
from utils import opentdb_questions_utils
from database.database_connection import Base, engine

def main():
    if not os.path.exists('config/api_request.json'):
        raise FileNotFoundError('config/api_request.json does not exist')
    with open('config/api_request.json', 'r') as file:
        data = json.load(file)

    if data['opentdb_questions'] == 0:
        opentdb_questions_utils.get_and_store_questions()
    if data['opentdb_categories'] == 0:
        opentdb_questions_utils.get_and_store_categories()
    if data['trivia_questions'] == 0:
        trivia_questions_utils.get_and_store_questions_and_categories()
    if data['quiz_questions'] == 0:
        quiz_questions_utils.get_and_store_questions_and_categories()

    with open('config/api_request.json', 'w') as file:
        data['opentdb_questions'] = 1
        data['opentdb_categories'] = 1
        data['trivia_questions'] = 1
        data['quiz_questions'] = 1
        json.dump(data, file, indent=4)

    # Create MySQL database tables
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    main()
