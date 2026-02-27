import os
import pandas as pd
from src import preprocess
from scripts.s02_ingest_vectors import ingest_movies 
from scripts.s01_run_preprocessing import run_preprocessing

# Get the directory where THIS script is located
# base_dir = os.path.dirname(os.path.abspath(__file__))

# Build the paths correctly
# movies_path = os.path.join(base_dir, "data", "raw", "tmdb_5000_movies.csv")
# credits_path = os.path.join(base_dir, "data", "raw", "tmdb_5000_credits.csv")

# print(f"Looking for: {movies_path}")
# preprocessed_df = run_preprocessing()

# print(preprocessed_df.head())



df = pd.read_csv('data/processed/tmdb_processed.csv')

# print(df.shape)
val = ingest_movies(df)

# print(df.head())

