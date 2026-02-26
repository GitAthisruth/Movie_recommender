import os
import sys

# 1. Get the directory of the current script (scripts/)
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
from src.logger import get_logger
from src.preprocess import clean_and_merge_data
logger = get_logger(__name__)

try:
    logger.info("Starting preprocessing script")

    # 1. Get the directory of the current script (scripts/)
    logger.debug(f"Current script directory: {current_script_dir}")

    # 2. Get the parent directory (Project Root)
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
    logger.debug(f"Ensured output directory exists: {output_dir}")

    processed_df.to_csv(output_file, index=False)
    logger.info("Preprocessing completed successfully")
    logger.info(f"Processed file saved at: {output_file}")

except Exception as e:
    logger.exception("Error occurred while running preprocessing script")
    sys.exit(1)