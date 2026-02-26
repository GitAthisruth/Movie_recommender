import pandas as pd
import ast
from src.logger import get_logger

logger = get_logger(__name__)

def convert_genres(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except Exception as e:
        logger.error(f"Error converting genres: {e}")
        return []

def convert_cast(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)][:3]
    except Exception as e:
        logger.error(f"Error converting cast: {e}")
        return []

def fetch_directors(text):
    try:
        for i in ast.literal_eval(text):
            if i['job'] == "Director":
                return [i['name']]
        return []
    except Exception as e:
        logger.error(f"Error fetching director: {e}")
        return []

def clean_and_merge_data(movies_path, credits_path):
    logger.info("Starting data cleaning and merging process")

    try:
        # Load datasets
        logger.info(f"Loading movies data from: {movies_path}")
        movies = pd.read_csv(movies_path)
        logger.info(f"Movies dataset loaded with shape: {movies.shape}")

        logger.info(f"Loading credits data from: {credits_path}")
        credits = pd.read_csv(credits_path)
        logger.info(f"Credits dataset loaded with shape: {credits.shape}")

        # Merge datasets
        logger.info("Merging movies and credits datasets")
        movies = movies.merge(credits, left_on='id', right_on='movie_id')
        logger.debug(f"Shape after merge: {movies.shape}")

        # Drop unnecessary columns
        movies.drop(columns=['movie_id', 'title_y'], inplace=True)
        movies.rename(columns={'title_x': 'title'}, inplace=True)

        # Select required columns
        movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        logger.debug(f"Shape after column selection: {movies.shape}")

        # Drop missing values
        before_drop = movies.shape[0]
        movies.dropna(inplace=True)
        after_drop = movies.shape[0]
        logger.info(f"Dropped {before_drop - after_drop} rows with missing values")

        # Parse JSON-like columns
        logger.info("Parsing genres, keywords, cast, and crew columns")
        movies['genres'] = movies['genres'].apply(convert_genres)
        movies['keywords'] = movies['keywords'].apply(convert_genres)
        movies['cast'] = movies['cast'].apply(convert_cast)
        movies['crew'] = movies['crew'].apply(fetch_directors)

        # Remove spaces for tag consistency
        logger.info("Removing spaces from tag fields")
        for col in ['genres', 'keywords', 'cast', 'crew']:
            movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

        # Process overview
        logger.info("Processing overview text")
        movies['overview'] = movies['overview'].apply(lambda x: x.split())

        # Create tags
        logger.info("Creating combined tags column")
        movies['tags'] = (movies['overview']+ movies['genres']+ movies['keywords']+ movies['cast']+ movies['crew'])

        # Final dataframe
        new_df = movies[['id', 'title', 'tags']].copy()
        new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

        logger.info(f"Final processed dataset shape: {new_df.shape}")
        logger.info("Data cleaning and merging completed successfully")

        return new_df

    except Exception as e:
        logger.exception("Error occurred during clean_and_merge_data")
        raise