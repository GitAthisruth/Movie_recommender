from src.preprocess import clean_and_merge_data
import os
# Get the directory where THIS script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

print("Starting preprocessing...")
processed_df = clean_and_merge_data(
    movies_path = os.path.join(base_dir, "data", "raw", "tmdb_5000_movies.csv"),
    credits_path = os.path.join(base_dir, "data", "raw", "tmdb_5000_credits.csv")
)

# Ensure output directory exists
os.makedirs(os.path.join(base_dir, "data", "processed"), exist_ok=True)
processed_df.to_csv(os.path.join(base_dir, "data", "processed", "tmdb_processed.csv"), index=False)
print("Preprocessing complete. Saved to data/processed/tmdb_processed.csv")