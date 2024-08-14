import json
import logging
import os.path
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Request
from routes import questions_route, categories_route, founders_route, admins_route

app = FastAPI()
@app.middleware('http')
async def log_rotation_middleware(request: Request, call_next):
    if not os.path.exists('config/logs.json'):
        raise FileNotFoundError('config/logs.json does not exist')

    with open('config/logs.json', 'r') as file:
        data = json.load(file)

    logging.basicConfig(filename=f'logs/app{data['app_value']}.log', level=logging.INFO, force=True)

    with open(f'logs/app{data['app_value']}.log', 'r') as file:
        if len(file.readlines()) >= 500:
            with open('config/logs.json', 'w') as config_file:
                data['app_value'] += 1
                json.dump(data, config_file, indent=4)
            logging.info(f'A new log file \'logs/app{data['app_value']}.log\' was created due to exceeding 500 lines in the current log file - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
            logging.basicConfig(filename=f'logs/app{data['app_value']}.log', level=logging.INFO, force=True)

    # Proceed to the next middleware or request handler
    response = await call_next(request)
    return response

@app.get('/')
async def root(request: Request):
    logging.info(f'Received request for {request.url} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
    return 'Hello World!'

app.include_router(questions_route.router, prefix='/questions', tags=['questions'])
app.include_router(categories_route.router, prefix='/categories', tags=['categories'])
app.include_router(founders_route.router, prefix='/founders', tags=['founders'])
app.include_router(admins_route.router, prefix='/admins', tags=['admins'])

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
