import psycopg2
import os
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", 5432),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME")
        )
        logger.info("PostgreSQL connection successful")
        return conn

    except Exception:
        logger.exception("Database connection failed")
        raise


def search_movies(vector_str, limit=5):
    """
    vector_str example:
    "[0.12, 0.45, 0.78, ...]"

    Uses pgvector cosine distance.
    Smaller distance = more similar.
    """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        sql = """
            SELECT title, tags
            FROM movies
            ORDER BY embedding <=> %s
            LIMIT %s;
        """

        cursor.execute(sql, (vector_str, limit))
        rows = cursor.fetchall()

        # Convert to dictionary format (like MySQL dictionary=True)
        results = []
        for row in rows:
            results.append({
                "title": row[0],
                "tags": row[1]
            })

        logger.info(f"Fetched {len(results)} movies")

        cursor.close()
        db.close()
        return results

    except Exception:
        logger.exception("Error in search_movies")
        raise