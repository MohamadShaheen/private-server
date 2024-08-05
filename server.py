from fastapi import FastAPI
from routes import questions

app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World!'

app.include_router(questions.router, prefix='/questions')
