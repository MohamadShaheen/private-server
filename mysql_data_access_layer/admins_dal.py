from fastapi import HTTPException
from database.models import User
from utils.hash_texts import hash_text, verify_text
from database.database_connection import SessionLocal

session = SessionLocal()

def get_user_by_id(id: int):
    db_user = session.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    return {
        'id': db_user.id,
        'username': db_user.username,
        'name': db_user.name,
    }

def get_user_by_username(username: str):
    db_user = session.query(User).filter(User.username == username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    return {
        'id': db_user.id,
        'username': db_user.username,
        'name': db_user.name,
    }

def get_users():
    db_users = session.query(User).all()

    if not db_users:
        raise HTTPException(status_code=404, detail='No users were found')

    users = {}
    for db_user in db_users:
        users[db_user.id] = {
            'username': db_user.username,
            'name': db_user.name,
        }

    return users
