import os
import sys

# 1. Get the directory of the current script (scripts/)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the parent directory (the Project Root)
project_root = os.path.dirname(current_script_dir)
# 3. Add the project root to sys.path so Python can see 'src'
if project_root not in sys.path:
    sys.path.append(project_root)


import pandas as pd
import mysql.connector
import json
from dotenv import load_dotenv

load_dotenv()# This looks for a .env file and loads the variables

from src.embedder import MovieEmbedder
embeder = MovieEmbedder()

# 2. Database Creation Logic
def setup_database():
    try:
        # Initial connection without a database name
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        
        db_name = os.getenv("DB_NAME")
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Create table if it doesn't exist
        # Note: 'VECTOR' type requires MySQL 8.0.39+ or TiDB/MariaDB equivalents.
        # If using standard local MySQL, we use LONGTEXT or BLOB for the vector.
        create_table_query = """
        CREATE TABLE IF NOT EXISTS movies (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            tags TEXT,
            embedding JSON
        )
        """
        cursor.execute(create_table_query)   
        return conn
    except Exception as e:
        sys.exit(1)

print("Loading processed data and initializing embedder...")
df = pd.read_csv(os.path.join(project_root, "data", "processed", "tmdb_processed.csv"))


db = setup_database()
cursor = db.cursor()

print("Generating vectors and inserting into database...")
insert_query = """   
INSERT INTO movies (movie_id,title,tags,embedding)
VALUES (%s,%s,%s,string_to_vectors(%s))
"""

# Limiting to 500 for a local test run. Remove `.head(500)` for the full dataset.
for _, row in df.head(500).iterrows():
    vector = embeder.encode(row['tags'])
    vector_str = json.dumps(vector)
    cursor.execute(insert_query, (row['id'], row['title'], row['tags'], vector_str))

db.commit()
cursor.close()
db.close()
print("Ingestion complete!")