import pandas as pd
import mysql.connector
import json
import os
from dotenv import load_dotenv
from src.embedder import MovieEmbedder

load_dotenv()

embeder = MovieEmbedder()


print("Loading processed data and initializing embedder...")
df = pd.read_csv('data/processed/tmdb_processed.csv')

db = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME") 
)

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
    cursor.execute(insert_query, (row['movie_id'], row['title'], row['tags'], vector_str))

db.commit()
cursor.close()
db.close()
print("Ingestion complete!")