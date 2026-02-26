import psycopg2
import os
import json
from dotenv import load_dotenv
import sys

load_dotenv()



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.logger import get_logger
from backend.database import get_db_connection , setup_database

logger = get_logger(__name__)

def ingest_movies(movies):
    """
    movies: list of dicts
    Example:
    {
        "title": "Avatar",
        "tags": "action adventure fantasy",
        "embedding": [0.12, 0.45, ...]
    }
    """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        setup_database(cursor)

        sql = """
            INSERT INTO movies (title, tags, embedding)
            VALUES (%s, %s, %s)
        """

        for movie in movies:
            vector_str = str(list(movie["embedding"]))  # pgvector format

            cursor.execute(
                sql,
                (
                    movie["title"],
                    movie["tags"],
                    vector_str
                )
            )

        db.commit()
        logger.info(f"Ingested {len(movies)} movies")

        cursor.close()
        db.close()

    except Exception:
        logger.exception("Error ingesting movies")
        raise


if __name__ == "__main__":
    # Example test data
    sample_movies = [
        {
            "title": "Movie A",
            "tags": "action adventure",
            "embedding": [0.1] * 384
        },
        {
            "title": "Movie B",
            "tags": "romance drama",
            "embedding": [0.2] * 384
        }
    ]

    ingest_movies(sample_movies)