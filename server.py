from fastapi import FastAPI
from routes import opentdb_questions_route, trivia_questions_route, quiz_questions_route

app = FastAPI()

@app.get('/')
async def root():
    return 'Hello World!'

app.include_router(opentdb_questions_route.router, prefix='/opentdb-questions', tags=['opentdb-questions'])
app.include_router(trivia_questions_route.router, prefix='/trivia-questions', tags=['trivia-questions'])
app.include_router(quiz_questions_route.router, prefix='/quiz-questions', tags=['quiz-questions'])
