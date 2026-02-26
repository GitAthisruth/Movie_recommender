import os
import sys
# 1. Get the directory of the current script (scripts/)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the parent directory (the Project Root)
project_root = os.path.dirname(current_script_dir)
# 3. Add the project root to sys.path so Python can see 'src'
if project_root not in sys.path:
    sys.path.append(project_root)

from src.preprocess import clean_and_merge_data

print("Starting preprocessing...")

movies_path = os.path.join(project_root, "data", "raw", "tmdb_5000_movies.csv")
credits_path = os.path.join(project_root, "data", "raw", "tmdb_5000_credits.csv")
output_dir = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_dir, "tmdb_processed.csv")

processed_df = clean_and_merge_data(movies_path, credits_path)
os.makedirs(output_dir, exist_ok=True)
processed_df.to_csv(output_file, index=False)
print("Preprocessing complete. Saved to data/processed/tmdb_processed.csv")