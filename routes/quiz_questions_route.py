import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from data_access_layer.quiz_questions_dal import *

router = APIRouter()
logging.basicConfig(filename='logs/quiz_questions_route.log', level=logging.INFO, force=True)

@router.get('/questions/')
async def questions():
    logging.info(f"Received request for /quiz-questions/questions/ endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    questions, length = get_questions()
    response = {
        'response': f'There are {length} questions. Showing random {len(questions)} questions',
        'questions': questions
    }
    logging.info(f"Request for /quiz-questions/questions/ endpoint was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response

@router.get('/random-question/')
async def random_question():
    logging.info(f"Received request for /quiz-questions/random-question/ endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    response = get_random_question()
    logging.info(f"Request for /quiz-questions/random-question/ endpoint was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response

@router.get('/questions-by-filter/')
async def questions_by_filter(type: Optional[str] = None, category: Optional[str] = None, difficulty: Optional[str] = None):
    logging.info(f"Received request for /quiz-questions/questions-by-filter/ endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    questions, length = get_questions_by_filter(type=type, category=category, difficulty=difficulty)

    if length == 0:
        logging.error(f"Error 404 in /quiz-questions/questions-by-filter/ - no questions were found due to wrong filter values - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
        detail = {
            'response': 'No questions found. One or more of the filters you provided does not satisfy the correct values.',
            'types': 'multiple',
            'difficulty': ['easy', 'medium', 'hard'],
            'categories': get_questions_categories()
        }
        raise HTTPException(status_code=404, detail=detail)

    response = {
        'response': f'There are {length} questions. Showing random {len(questions)} questions',
        'questions': questions
    }
    logging.info(f"Request for /quiz-questions/questions-by-filter/ endpoint was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response
