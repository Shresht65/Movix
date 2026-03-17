
import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommender System")

# ---------------- TMDB API ----------------
API_KEY = "9a669c38a1e507152aceb4993222ab23"

# ---------------- LOAD DATA ----------------
@st.cache_resource
def load_data():
    BASE_DIR = os.path.dirname(__file__)

    movies_path = os.path.join(BASE_DIR, "movies_dict.pkl")
    similarity_path = os.path.join(BASE_DIR, "similarity_small.pkl")

    movies_dict = pickle.load(open(movies_path, "rb"))
    movies = pd.DataFrame(movies_dict)

    similarity_topk = pickle.load(open(similarity_path, "rb"))

    return movies, similarity_topk

movies, similarity_topk = load_data()

# ---------------- FETCH POSTER ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        data = requests.get(url).json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return None
    except:
        return None

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    similar_movies = similarity_topk[movie_index]

    recommended_movies = []
    recommended_posters = []

    for i in similar_movies:

        movie_id = movies.iloc[i].movie_id
        poster = fetch_poster(movie_id)

        if poster:
            recommended_movies.append(movies.iloc[i].title)
            recommended_posters.append(poster)

        if len(recommended_movies) == 6:
            break

    return recommended_movies, recommended_posters

# ---------------- UI ----------------
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

# ---------------- BUTTON ----------------
if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    cols = st.columns(len(names))

    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])