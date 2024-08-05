from typing import Optional
from fastapi import APIRouter, HTTPException
from data_access_layer.questions import *

router = APIRouter()

@router.get('/')
async def questions():
    return get_questions()

@router.get('/random-question/')
async def random_question():
    return get_random_question()

@router.get('/questions-by-filter/')
async def questions_by_filter(type: Optional[str] = None, category: Optional[str] = None, difficulty: Optional[str] = None):
    response = get_questions_by_filter(type=type, category=category, difficulty=difficulty)

    if len(response) == 0:
        detail = {
            'response': 'No questions found. One or more of the filters you provided does not satisfy the correct values.',
            'types': ['boolean', 'multiple'],
            'difficulty': ['easy', 'medium', 'hard'],
            'categories': get_questions_categories()
        }
        raise HTTPException(status_code=404, detail=detail)

    return response
