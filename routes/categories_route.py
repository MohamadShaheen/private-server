import logging
from datetime import datetime
from fastapi import APIRouter
from mongodb_data_access_layer.categories_dal import get_questions_categories

router = APIRouter()

@router.get('/')
def categories():
    logging.info(f"Received request for /categories/ endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    response = get_questions_categories()
    logging.info(f"Request for /categories/ endpoint was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response
