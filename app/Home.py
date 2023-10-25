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

N=20 #number of recommendations

#page config
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="centered",
)

# list of rated movies by current user
st.session_state.setdefault('ratings', pd.DataFrame(columns=['movieId', 'rating']).set_index('movieId'))
# selected genre list
st.session_state.setdefault('genres', [])
# should the rated movies be hidden
st.session_state.setdefault('hide_rated', False)
# current page number
st.session_state.setdefault('page_no', 1)
# page to be displayed
st.session_state.setdefault('page', 'homepage')

# load images from tmdb api
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

# load data from storage
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

    genres = metadata['genres'].str.split(',').explode().unique().tolist()

    return metadata, collaborative_similarity, content_similarity, genres
metadata, collaborative_similarity, content_similarity, genres = load_data()

# get movies with all provided genres
@st.cache_resource
def get_movies_with_all_genres(genres):
    _movies = metadata
    _movies.dropna(subset=['genres'], inplace=True)
    for genre in genres:
        _movies = _movies[_movies['genres'].str.contains(genre)]

    return _movies["movieId"].tolist()

# get recommendations based on rated movies
def recommend(movies=None, genres=[], hide_rated=True, n=20, page=0):
    # weights for collaborative and content based similarity
    CONTENT_W = 0.5
    COLLAB_W = 0.5

    movie_similarities = pd.DataFrame()
    
    # if no movies are rated, return top rated movies
    if movies.shape[0] == 0:
        movie_similarities = metadata[['movieId', 'order']].sort_values(by='order', ascending=False).reset_index(drop=True)
    
    # else calculate similarity scores
    else:
        # iterate through rated movies
        for movie_id, rating in movies.iterrows():
            # score with item based collabarative similarity
            collaborative_score = collaborative_similarity.get(movie_id, 0)

            # score with content based similarity
            content_score = content_similarity.get(movie_id, 0)

            # add weighted score to dataframe
            # similarity = (collaborative_score * COLLAB_W + content_score * CONTENT_W) * (rating - 2.5)
            movie_similarities = pd.concat(
                [movie_similarities, (collaborative_score * COLLAB_W + content_score * CONTENT_W) * (float(rating) - 2.5)], axis=1)

        # sum similarity scores for each movie
        movie_similarities = movie_similarities.sum(axis=1)

        # hide already rated movies if requested
        if hide_rated:
            movie_similarities = movie_similarities.drop(movies.index)

        # sort similarity with the calculated score
        movie_similarities = movie_similarities.sort_values(ascending=False).reset_index().rename(columns={0: 'score', 'index': 'movieId'})

    #filter by genres provided
    if len(genres) > 0:
        movies = get_movies_with_all_genres(genres)
        movie_similarities = movie_similarities[movie_similarities['movieId'].isin(movies)]
        movie_similarities.reset_index()
        
    # make subset of movies based on number of recommendation (n) and page number (page)
    movie_similarities = movie_similarities[(page-1)*n:page*n]

    return movie_similarities

# function to update session variables
def update_session(dic):
    for key, value in dic.items():
        st.session_state[key] = value

def homepage():
    st.title('Movie Recommender System')
    st.write('Rate some movies to get started!')

    # filter form
    with st.form(key='filter') as form:
        selected_genres = st.multiselect('Genres', genres, key='genre_select', default=st.session_state['genres'])
        hide_rated_checkbox = st.checkbox('Hide Rated Movies', key='hide_rated_chk', value=st.session_state['hide_rated'])
        submit_button = st.form_submit_button(label='Submit')

    # if form is submitted update session variables
    if submit_button:
        st.session_state['genres'] = selected_genres
        st.session_state['hide_rated'] = hide_rated_checkbox
        st.session_state['page_no'] = 1

    # get recommendations
    recommendations = recommend(
        movies=st.session_state['ratings'],
        hide_rated=st.session_state['hide_rated'],
        genres=st.session_state['genres'],
        n=N,
        page=st.session_state['page_no']
        )
    
    # get a list of movies from recommendations
    movies = []
    for i in recommendations.index:
        try:
            movie = metadata[metadata['movieId'] == recommendations.loc[i, 'movieId']].iloc[0]
        except:
            continue
        movies.append(movie)

    # display movies in a grid 4x4
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

    # pagination
    prev_page_col, next_page_col = st.columns(2)
    prev_page_col.button(
            "⬅️ Previous Page", 
            key='prev_page', 
            on_click = lambda x={'page_no': st.session_state['page_no'] - 1}: update_session(x),
            use_container_width=True,
            disabled=st.session_state['page_no'] == 1)

    next_page_col.button(
            "➡️ Next Page", 
            key='next_page', 
            on_click = lambda x={'page_no': st.session_state['page_no'] + 1}: update_session(x),
            use_container_width=True,
            disabled=len(recommendations) < N)

    # asynchronously load images
    load_images(images)

def movie_view():
    # button to go back to home page
    st.button("⬅️ Back to Homepage", on_click = lambda x={'page': 'homepage'}: update_session(x))

    # retrive movies metadata
    movie = metadata[metadata['movieId'] == st.session_state['movie']]
    
    # display movie poster and info
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

    # add new rating to session variables
    if stars > 0:
        st.session_state['ratings'].loc[st.session_state['movie']] = stars

    st.session_state['page_no'] = 1

if st.session_state['page'] == 'homepage':
    homepage()
elif st.session_state['page'] == 'movie_view':
    movie_view()