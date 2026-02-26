import os
import pandas as pd
from src import preprocess

# Get the directory where THIS script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Build the paths correctly
movies_path = os.path.join(base_dir, "data", "raw", "tmdb_5000_movies.csv")
credits_path = os.path.join(base_dir, "data", "raw", "tmdb_5000_credits.csv")

print(f"Looking for: {movies_path}")
df = preprocess.clean_and_merge_data(movies_path, credits_path)

print(df.head())