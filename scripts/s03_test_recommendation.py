import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.embedder import MovieEmbedder
from backend.database import search_movies
from src.logger import get_logger

logger = get_logger(__name__)


def test_recommendation(query_text):
    try:
        logger.info(f"User query: {query_text}")

        embedder = MovieEmbedder()
        query_vector = embedder.encode(query_text)
        # pgvector expects string format
        vector_str = str(query_vector)
        results = search_movies(vector_str,limit=5)
        print("\nTop Recommendations:\n")
        for i, movie in enumerate(results, 1):
            print(f"{i}. {movie['title']}")    

    except Exception:
        logger.exception("Recommendation test failed")
        raise   


if __name__ == "__main__":
    user_query = input("Enter movie type (e.g., action comedy romance): ")
    test_recommendation(user_query)