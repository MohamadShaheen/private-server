from typing import Optional
from fastapi import APIRouter, HTTPException
from data_access_layer.trivia_questions_dal import *

router = APIRouter()

@router.get('/questions/')
async def questions():
    questions, length = get_questions()
    response = {
        'response': f'There are {length} questions. Showing random {len(questions)} questions',
        'questions': questions
    }
    return response

@router.get('/random-question/')
async def random_question():
    return get_random_question()

@router.get('/questions-by-filter/')
async def questions_by_filter(type: Optional[str] = None, category: Optional[str] = None, difficulty: Optional[str] = None):
    questions, length = get_questions_by_filter(type=type, category=category, difficulty=difficulty)

    if length == 0:
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
    return response
