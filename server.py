import json
import logging
import os.path
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from routes import questions_route

app = FastAPI()
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
        logging.info(f'A new log file \'logs/app{data['app_value']}.log\' was created due to exceeding 500 lines in the current log file - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        logging.basicConfig(filename=f'logs/app{data['app_value']}.log', level=logging.INFO, force=True)

@app.get('/')
async def root():
    logging.info(f"Received request for 'root' endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return 'Hello World!'

app.include_router(questions_route.router, prefix='/questions', tags=['questions'])

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
