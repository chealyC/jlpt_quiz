import sqlite3
import random
from vocab import add_vocab


def get_quiz_question():

    add_vocab()

    connection = sqlite3.connect("jlpt.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, word, reading, meaning, score, usage
        FROM vocabulary
    """)

    rows = cursor.fetchall()

    connection.close()

    if not rows:
        return {"error": "No vocabulary found"}

    # Higher score = more likely to appear
    weights = [row[4] for row in rows]

    result = random.choices(rows, weights=weights, k=1)[0]

    readings = [
        reading.strip()
        for reading in result[2].split(";")
    ]

    meanings = [
        meaning.strip()
        for meaning in result[3].split(";")
    ]

    usage = result[5]

    return {
        "id": result[0],
        "word": result[1],
        "reading": result[2],
        "meaning": result[3],
        "readings": readings,
        "meanings": meanings,
        "usage" : usage
    }