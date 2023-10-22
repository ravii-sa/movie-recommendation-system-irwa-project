import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from math import ceil
from streamlit_star_rating import st_star_rating

load_dotenv()

API_KEY = os.getenv('TMDB_API_KEY')
DEFAULT_POSTER = "data:image/jpeg;base64,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"
COLLAB_CONTENT_RATIO = 0.5

#page config
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="centered",
)

st.session_state.setdefault('ratings', [])

def load_images(images):
    async def fetch_posters(movies):
        async with aiohttp.ClientSession() as session:
            for movie_id, image in movies.items():
                url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
                poster_url = await fetch_movie_poster(session, url)
                image.image(poster_url, use_column_width=True)

    async def fetch_movie_poster(session, url):
        try:
            async with session.get(url) as response:
                data = await response.json()
                poster_url = "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
                return poster_url
        except Exception as e:
            return DEFAULT_POSTER

    asyncio.run(fetch_posters(images))

@st.cache_resource
def load_data():
    import pickle
    import os

    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')

    metadata = pd.read_csv(os.path.join(exports_dir, 'metadata.csv'))

    with open(os.path.join(exports_dir, 'collaborative_similarity.pkl'), 'rb') as f:
        collaborative_similarity = pickle.load(f)

    with open(os.path.join(exports_dir, 'content_similarity.pkl'), 'rb') as f:
        content_similarity = pickle.load(f)

    return metadata, collaborative_similarity, content_similarity

metadata, collaborative_similarity, content_similarity = load_data()

def recommend(movies=[], n=20):

    if len(movies) == 0:
        df = metadata.sort_values('order', ascending=False)[:n]
        return list(zip(df['movieId'], df['order']))
    
    movie_ids = [movie[0] for movie in movies]
    ratings = [movie[1] - 2.5 for movie in movies]

    movie_similarities = (content_similarity.get(movie_ids, 0) * (1 - COLLAB_CONTENT_RATIO) + 
                          collaborative_similarity.get(movie_ids, 0) * COLLAB_CONTENT_RATIO) * ratings
    movie_similarities = movie_similarities.sum(axis=1)

    movie_similarities = sorted(list(zip(movie_similarities.index, movie_similarities)), key=lambda x: x[1], reverse=True)
    
    return movie_similarities[:n]

def update_session(dic):
    for key, value in dic.items():
        st.session_state[key] = value

def homepage():
    st.title('Movie Recommender System')

    recommendations = recommend(movies=st.session_state['ratings'], n=20)
    movies = []

    for movie_id, rating in recommendations:
        movies.append(metadata[metadata['movieId'] == movie_id].iloc[0])

    cols = []
    for i in range(ceil(len(movies) / 4)):
        cols.extend(st.columns(4))

    images = dict()

    for i in range(len(movies)):
        movie = movies[i]
        image = cols[i].image(DEFAULT_POSTER, use_column_width=True)
        images[movie['tmdbId']] = image
        col1, col2 = cols[i].columns([5, 2])
        col1.write(movie['title'])
        col2.button("ℹ️", key=movie['movieId'], on_click = lambda x={'movie': movie['movieId'], 'page': 'movie_view'}: update_session(x))

    load_images(images)

def movie_view():
    st.button("⬅️ Back to Homepage", on_click = lambda x={'page': 'homepage'}: update_session(x))

    movie = metadata[metadata['movieId'] == st.session_state['movie']]
    
    image_col, info_col = st.columns(2)

    image = image_col.image(DEFAULT_POSTER, use_column_width=True)
    load_images({movie['tmdbId'].values[0]: image})

    with info_col:
        st.title(movie['title'].values[0])
        st.write(f"Genres: {movie['genres'].values[0]}")
        st.write(f"Release Date: {movie['release_date'].values[0]}")
        st.write(f"Runtime: {movie['runtime'].values[0]} minutes")
        st.write(f"Average Rating: {movie['vote_average'].values[0]}")
        stars = st_star_rating("", maxValue=5, defaultValue=0, key="rating")

    st.write(movie['overview'].values[0])

    if stars > 0:
        st.session_state['ratings'].append((movie['movieId'].values[0], stars))

if 'page' not in st.session_state:
    st.session_state['page'] = 'homepage'

if st.session_state['page'] == 'homepage':
    homepage()
elif st.session_state['page'] == 'movie_view':
    movie_view()