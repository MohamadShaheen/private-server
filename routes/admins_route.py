import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from mysql_data_access_layer import admins_dal

router = APIRouter()

@router.get('/users/')
async def get_users(request: Request):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = admins_dal.get_users()
        logging.info(
            f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(
            f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e

@router.get('/users/user-by-id/')
async def get_user_by_id(request: Request, id: int):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = admins_dal.get_user_by_id(id)
        logging.info(
            f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(
            f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e
