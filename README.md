# Introduction

In this project we fetch questions from [OpenTDB](https://opentdb.com/api_config.php), [TriviaAPI](https://the-trivia-api.com/docs/v2/) and [QuizAPI](https://quizapi.io/docs/1.0/overview) and store them into [MongoDB](https://www.mongodb.com/try/download/shell). These question then used to serve FastAPI endpoints for multiple purposes.

# Instructions

- In order to fetch the [QUIZ_TOKEN](#installation) environment variable you need to [signup](https://quizapi.io/register) in their website and then [get the api token](https://quizapi.io/clientarea/settings/token).

# Features

- Get all questions.
- Get random question.
- Get questions by filter.

# Technologies Used

- FastAPI
- MongoDB
- Uvicorn

# Requirements

- Python 3.8+
- MongoDB Server

# Installation

1. **Clone the repository:**
   ```shell
    git clone https://github.com/MohamadShaheen/private-server.git
    cd private-server
    ```
   
2. **Setup the virtual environment:**
   ```shell
   python -m venv venv
   venv/Scripts/activate # On Mac/Linux `source venv/bin/activate`
    ```
   
3. **Install dependencies:**
    ```shell
    pip install -r requirements.txt
    ```
   
4. **Set up environment variables:** Create a `.env` file in the project root directory and add the following environment variables:
    ```shell
    MONGODB_URL=<your-mongodb-connection-string> # For example: `mongodb://localhost:27017/`
    QUIZ_TOKEN=<your-quiz-api-token>
    ```
   
# Project Logs

Make sure to create a directory named `logs` in the project root directory:
   ```shell
   mkdir "logs"
   ```

# Fetching Questions and Storing into Database

1. Make sure `config/api_request.json` values are set to 0.
2. Run `main.py`:
    ```shell
    python main.py
    ```

# Running the Server

You can run the server in any of the following ways:
1. ```shell
   uvicorn server:app
   ```
2. ```shell
   python server.py
   ```

# Questions Database

There are two types of questions, `multiple` and `boolean`. The questions are represented in the database in the following form:

- Boolean questions:

```json
{
  "_id": {
    "$oid": "66b4d3cb9efdafc18501d22d"
  },
  "type": "boolean",
  "difficulty": "easy",
  "category": "History",
  "question": "The Spitfire originated from a racing plane.",
  "correct_answer": "True",
  "incorrect_answers": [
    "False"
  ]
}
```

- Multiple questions:

```json
{
  "_id": {
    "$oid": "66a4ec1101b1d98e4f482e00"
  },
  "type": "multiple",
  "difficulty": "easy",
  "category": "General Knowledge",
  "question": "What airline was the owner of the plane that crashed off the coast of Nova Scotia in 1998?",
  "correct_answer": "Swiss Air",
  "incorrect_answers": [
    "Air France",
    "British Airways",
    "TWA"
  ]
}
```