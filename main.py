from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import vocab
import questions
import sqlite3


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/quiz/")
def get_quiz_question():
    return questions.get_quiz_question()


class Answer(BaseModel):
    id: int
    correct: bool


@app.post("/quiz/answer/")
def submit_answer(answer: Answer):

    connection = sqlite3.connect("jlpt.db")
    cursor = connection.cursor()

    if answer.correct:

        cursor.execute("""
            UPDATE vocabulary
            SET score = MAX(1, score - 1)
            WHERE id = ?
        """, (answer.id,))

    else:

        cursor.execute("""
            UPDATE vocabulary
            SET score = MIN(10, score + 2)
            WHERE id = ?
        """, (answer.id,))

    connection.commit()
    connection.close()

    return {"message": "Score updated"}