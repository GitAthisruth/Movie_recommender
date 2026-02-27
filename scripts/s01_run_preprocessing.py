import os
import sys
from src.logger import get_logger
from src.preprocess import clean_and_merge_data

logger = get_logger(__name__)


def run_preprocessing(project_root=None):
    """
    Runs the preprocessing pipeline and returns the processed dataframe.
    
    Parameters:
        project_root (str, optional): Root directory of the project.
                                      If None, it will be auto-detected.
    
    Returns:
        processed_df (pd.DataFrame)
    """

    try:
        logger.info("Starting preprocessing function")

        # Detect project root if not provided
        if project_root is None:
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_script_dir)

        logger.debug(f"Project root directory: {project_root}")

        # File paths
        movies_path = os.path.join(project_root, "data", "raw", "tmdb_5000_movies.csv")
        credits_path = os.path.join(project_root, "data", "raw", "tmdb_5000_credits.csv")
        output_dir = os.path.join(project_root, "data", "processed")
        output_file = os.path.join(output_dir, "tmdb_processed.csv")

        logger.info(f"Movies path: {movies_path}")
        logger.info(f"Credits path: {credits_path}")
        logger.info(f"Output path: {output_file}")

        # Run preprocessing
        logger.info("Running clean_and_merge_data()")
        processed_df = clean_and_merge_data(movies_path, credits_path)

        logger.info(f"Processed dataframe shape: {processed_df.shape}")

        # Save output
        os.makedirs(output_dir, exist_ok=True)
        processed_df.to_csv(output_file, index=False)

        logger.info("Preprocessing completed successfully")
        logger.info(f"Processed file saved at: {output_file}")

        return processed_df

    except Exception as e:
        logger.exception("Error occurred while running preprocessing")
        raise