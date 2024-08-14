import logging
from datetime import datetime
from fastapi import APIRouter, Request
from mongodb_data_access_layer.categories_dal import get_questions_categories

router = APIRouter()

@router.get('/')
async def categories(request: Request):
    logging.info(f"Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    response = get_questions_categories()
    logging.info(f"Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return response
