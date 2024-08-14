import logging
from typing import Optional
from datetime import datetime
from mongodb_data_access_layer.questions_dal import *
from fastapi import APIRouter, HTTPException, Request
from mongodb_data_access_layer.categories_dal import get_questions_categories

router = APIRouter()

@router.get('/random-question/')
async def random_question(request: Request):
    logging.info(f"Received request for /questions/random-question/ endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    response = get_random_question()
    logging.info(f"Request for /questions/random-question/ endpoint was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response

@router.get('/filter/')
async def questions_by_filter(request: Request, type: Optional[str] = None, category: Optional[str] = None, difficulty: Optional[str] = None):
    logging.info(f"Received request for /questions/filter/ endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    questions, length = get_questions_by_filter(type=type, category=category, difficulty=difficulty)

    if length == 0:
        logging.error(f"Error 404 in /questions/filter/ - no questions were found due to wrong filter values - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
        detail = {
            'response': 'No questions found. One or more of the filters you provided does not satisfy the correct values, or there are 0 questions for the provided values.',
            'types': 'multiple',
            'difficulty': ['easy', 'medium', 'hard'],
            'categories': get_questions_categories()
        }
        raise HTTPException(status_code=404, detail=detail)

    response = {
        'response': f'There are {length} questions. Showing random {len(questions)} questions',
        'questions': questions
    }
    logging.info(f"Request for /questions/filter/ endpoint was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response
