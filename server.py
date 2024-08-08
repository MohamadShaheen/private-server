import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from routes import questions_route

app = FastAPI()
logging.basicConfig(filename='logs/app.log', level=logging.INFO, force=True)

@app.get('/')
async def root():
    logging.info(f"Received request for 'root' endpoint - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]")
    return 'Hello World!'

app.include_router(questions_route.router, prefix='/questions', tags=['questions'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
