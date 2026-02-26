import mysql.connector
import os
from dotenv import load_dotenv
from src.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        logger.info("Database connection successful")
        return conn

    except Exception as e:
        logger.exception("Database connection failed")
        raise


def search_movies(vector_str, limit=5):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        sql = """
            SELECT title, tags
            FROM movies
            ORDER BY VECTOR_DISTANCE(embedding, string_to_vector(%s))
            LIMIT %s;
        """

        cursor.execute(sql, (vector_str, limit))
        results = cursor.fetchall()

        logger.info(f"Fetched {len(results)} movies")

        cursor.close()
        db.close()
        return results

    except Exception as e:
        logger.exception("Error in search_movies")
        raise