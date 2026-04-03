import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.src.embedder import MovieEmbedder
from backend.database import search_movies

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedder = MovieEmbedder()

class Query(BaseModel):
    text: str
    limit: int = 15

@app.post("/api/recommend")
def recommend_movies(query: Query):
    try:
        query_vector = embedder.encode(query.text)
        vector_str = str(query_vector)
        results = search_movies(vector_str, limit=query.limit)
        
        # Enrich with Tavily images and descriptions
        from backend.src.data_scrapper import fetch_web_data
        for movie in results:
            try:
                # Query tavily for a movie poster image and short description
                t_data = fetch_web_data(f"{movie['title']} movie official poster")
                movie['image'] = t_data['images'][0] if t_data.get('images') else None
                movie['description'] = t_data['descriptions'][0] if t_data.get('descriptions') else ""
            except Exception:
                movie['image'] = None
                movie['description'] = ""
                
        return {"movies": results, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

# Mount the static files (frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
