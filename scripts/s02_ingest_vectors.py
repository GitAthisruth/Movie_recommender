import os
from dotenv import load_dotenv
import sys

load_dotenv()



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.logger import get_logger
from backend.database import get_db_connection , setup_database
from src.embedder import MovieEmbedder

logger = get_logger(__name__)

def ingest_movies(movies_df):

    try:
        logger.info("Starting movie ingestion")

        # Initialize embedder
        embedder = MovieEmbedder()

        # Convert dataframe to records
        movies = movies_df.to_dict(orient="records")

        # Extract tags for batch embedding (faster)
        tags_list = [movie["tags"] for movie in movies]

        logger.info("Generating embeddings...")
        embeddings = embedder.encode(tags_list)

        # Add embeddings back to records
        for movie, emb in zip(movies, embeddings):
            movie["embedding"] = emb

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

