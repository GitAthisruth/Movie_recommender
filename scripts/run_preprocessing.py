from src.preprocess import clean_and_merge_data
import os

print("Starting preprocessing...")
processed_df = clean_and_merge_data(
    movies_path= "/data/raw/tmdb_5000_movies.csv",
    credits_path= "/data/raw/tmdb_5000_credits.csv"
)

# Ensure output directory exists
os.makedirs('data/processed', exist_ok=True)
processed_df.to_csv('data/processed/tmdb_processed.csv', index=False)
print("Preprocessing complete. Saved to data/processed/tmdb_processed.csv")