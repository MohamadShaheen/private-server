import logging
from datetime import datetime
from mysql_data_access_layer import founders_dal
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.get('/admins/')
async def get_admins(request: Request):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.get_admins()
        logging.info(f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e
    
@router.get('/')
async def get_founders(request: Request):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.get_founders()
        logging.info(f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e
    
@router.post('/add-admin/')
async def add_admin(request: Request, id: int, username: str, name: str, password: str):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.add_admin(id, username, name, password)
        logging.info(f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e

@router.delete('/delete-admin/')
async def delete_admin(request: Request, id: int, username: str):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.delete_admin(id, username)
        logging.info(f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return 'admin was deleted successfully'
    except HTTPException as e:
        logging.error(f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e

@router.put('/edit-admin/')
async def edit_admin(request: Request, old_id: int, old_username: str, new_id: int = None, new_username: str = None, new_name: str = None, new_password: str = None):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.edit_admin(old_id, old_username, new_id, new_username, new_name, new_password)
        logging.info(f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e

@router.post('/')
async def add_founder(request: Request, id: int, username: str, name: str, password: str):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.add_founder(id, username, name, password)
        logging.info(
            f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(
            f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e

@router.get('/verify-founder/')
async def verify_founder(request: Request, id: int, username: str, password: str):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    try:
        response = founders_dal.verify_founder(id, username, password)
        logging.info(
            f'Request for {request.url} was processed successfully - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        return response
    except HTTPException as e:
        logging.error(
            f'{e} - occurred while getting {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        raise e
