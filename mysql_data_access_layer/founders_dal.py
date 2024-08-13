from sqlalchemy import or_
from fastapi import HTTPException
from database.models import Admin, Founder
from utils.hash_texts import hash_text, verify_text
from database.database_connection import SessionLocal

session = SessionLocal()

def add_admin(id: int, username: str, name: str, password: str):
    db_admin = session.query(Admin).filter(Admin.id == id).first()

    if db_admin:
        raise HTTPException(status_code=409, detail='Admin already exists')

    admin_data = {
        'id': id,
        'username': username,
        'name': name,
        'password': password
    }

    db_admin = Admin(**admin_data)
    session.add(db_admin)
    session.commit()
    session.close()

    return db_admin

def delete_admin(id: int, username: str):
    db_admin = session.query(Admin).filter(Admin.id == id).first()

    if not db_admin:
        raise HTTPException(status_code=404, detail='Admin does not exist')

    if username != db_admin.username:
        raise HTTPException(status_code=403, detail='Admin username does not match')

    session.delete(db_admin)
    session.commit()
    session.close()

def edit_admin(old_id: int, old_username: str, new_id: int = None, new_username: str = None, new_name: str = None, new_password: str = None):
    db_admin = session.query(Admin).filter(Admin.id == old_id).first()

    if not db_admin:
        raise HTTPException(status_code=404, detail='Admin does not exist')

    if old_username != db_admin.username:
        raise HTTPException(status_code=403, detail='Admin username does not match')

    db_admin_query = session.query(Admin).filter(or_(Admin.id == new_id, Admin.username == new_username)).first()

    if db_admin_query:
        raise HTTPException(status_code=409, detail='Admin already exists')

    if new_id is not None:
        db_admin.id = new_id
    if new_username is not None:
        db_admin.username = new_username
    if new_name is not None:
        db_admin.name = new_name
    if new_password is not None:
        db_admin.password = new_password

    session.commit()
    session.close()

    return {
        'id': new_id,
        'username': new_username,
        'name': new_name,
        'password': new_password
    }

def get_admins():
    db_admins = session.query(Admin).all()

    if not db_admins:
        raise HTTPException(status_code=404, detail='No admins were found')

    admins = {}
    for db_admin in db_admins:
        admins[db_admin.id] = {
            'username': db_admin.username,
            'name': db_admin.name,
            'password': db_admin.password
        }

    return admins

def delete_admins():
    db_admins = session.query(Admin).all()

    if not db_admins:
        raise HTTPException(status_code=404, detail='No admins were found')

    for db_admin in db_admins:
        delete_admin(db_admin.id, db_admin.username)

def add_founder(id: int, username: str, name: str, password: str):
    db_founder = session.query(Founder).filter(Founder.id == id).first()

    if db_founder:
        raise HTTPException(status_code=409, detail='Founder already exists')

    founder_data = {
        'id': id,
        'username': username,
        'name': name,
        'password': hash_text(password)
    }

    db_founder = Admin(**founder_data)
    session.add(db_founder)
    session.commit()
    session.close()

    return db_founder

def get_founders():
    db_founders = session.query(Founder).all()

    if not db_founders:
        raise HTTPException(status_code=404, detail='No founders were found')

    founders = {}
    for db_founder in db_founders:
        founders[db_founder.id] = {
            'username': db_founder.username,
            'name': db_founder.name,
        }

    return founders

def verify_founder(id: int, username: str, password: str):
    db_founder = session.query(Founder).filter(Founder.id == id).first()

    if not db_founder:
        raise HTTPException(status_code=404, detail='Founder does not exist')

    if username != db_founder.username:
        raise HTTPException(status_code=403, detail='Founder username does not match')

    if not verify_text(plain_text=password, hashed_text=db_founder.password):
        raise HTTPException(status_code=403, detail='Founder password does not match')
