import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

def create_user(user_id, username, password):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (id, username, password) VALUES (%s, %s, %s)",
        (user_id, username, password)
    )
    conn.commit()

def get_user_by_username(username):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, password FROM users WHERE username=%s",
        (username,)
    )
    return cur.fetchone()

def get_user_preferences(user_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT preferences FROM user_preferences WHERE user_id=%s",
        (user_id,)
    )
    row = cur.fetchone()
    return row[0] if row else []

def save_user_preference(user_id, preference):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO user_preferences (user_id, preferences)
        VALUES (%s, ARRAY[%s])
        ON CONFLICT (user_id)
        DO UPDATE SET preferences =
        CASE
            WHEN NOT %s = ANY(user_preferences.preferences)
            THEN array_append(user_preferences.preferences, %s)
            ELSE user_preferences.preferences
        END
        """,
        (user_id, preference, preference, preference)
    )
    conn.commit()
