import os

from dotenv import load_dotenv
from psycopg import connect

load_dotenv()


def get_db_connection():
    return connect(os.environ["DATABASE_URL"])


def insert_message(user_id: str, conversation_id: str, message: str) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO messages (user_id, conversation_id, message)
                VALUES (%s, %s, %s)
                """,
                (user_id, conversation_id, message),
            )
