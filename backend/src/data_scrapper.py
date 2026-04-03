import os
from dotenv import load_dotenv
from tavily import TavilyClient

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

def fetch_web_data(query: str):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")

    tavily_client = TavilyClient(api_key=api_key)
    
    # search with include_images=True
    response = tavily_client.search(query, include_images=True, max_results=3)
    
    images = response.get("images", [])
    descriptions = [res.get("content") for res in response.get("results", [])]
    
    return {
        "images": images,
        "descriptions": descriptions,
        "raw_response": response
    }