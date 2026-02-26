import pandas as pd
import ast

def convert_genres(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert_cast(text):
    return [i['name'] for i in ast.literal_eval(text)][:3]

def fetch_directors(text):
    for i in ast.literal_eval(text):
        if i['job'] == "Director":
            return [i['name']]
    return []


def clean_and_merge_data(movies_path, credits_path):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    
    # Merge and filter
    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)
    
    # Parse strings to lists
    movies['genres'] = movies['genres'].apply(convert_list)
    movies['keywords'] = movies['keywords'].apply(convert_list)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)
    
    # Remove spaces for unique tags
    for col in ['genres', 'keywords', 'cast', 'crew']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])
        
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    # Create final tags
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    new_df = movies[['movie_id', 'title', 'tags']].copy()
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())
    
    return new_df
