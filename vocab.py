import sqlite3
from vocabulary_data import vocabulary

def create_table():
    connection = sqlite3.connect("jlpt.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL UNIQUE,
            reading TEXT NOT NULL,
            meaning TEXT NOT NULL,
            score INTEGER DEFAULT 3,
            usage TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_vocab():
    create_table()

    connection = sqlite3.connect("jlpt.db")
    cursor = connection.cursor()

    for word in vocabulary:

        if len(word) == 3:

            cursor.execute("""
                INSERT OR IGNORE INTO vocabulary
                (word, reading, meaning)
                VALUES (?, ?, ?)
            """, word)

        elif len(word) == 4:

            cursor.execute("""
                INSERT INTO vocabulary
                (word, reading, meaning, usage)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(word) DO UPDATE SET
                    usage = excluded.usage
            """, word)

    connection.commit()
    connection.close()

def get_vocab():
    add_vocab()

    connection = sqlite3.connect("jlpt.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM vocabulary
    """)

    results = cursor.fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "word": row[1],
            "reading": row[2],
            "meaning": row[3]
        }
        for row in results
    ]

