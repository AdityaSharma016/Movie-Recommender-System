import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np



def fetch_poster(movie_id):
    api_key = "11940ff42429b028d3c93aca8a3c5a13"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Network+Error"


def recommend(movies_name):

    movie_index = np.where(movies_list['title'] == movies_name)[0][0]

    distances = similarity[movie_index]
    movie_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movie_list_sorted:
        # Get the movie ID safely using integer row position (.iloc)
        movie_id = movies_list.iloc[i[0]].movie_id

        recommend_movies.append(movies_list.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters
try:
    movies_list = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(
        f"Could not find data files! Make sure 'movies.pkl' and 'similarity.pkl' are in the same folder as this script. Error: {e}")

st.title('Movie Recommender System')


if 'movies_list' in locals() and 'similarity' in locals():
    selected_movies_name = st.selectbox(
        "Select a movie to get recommendations:",
        movies_list['title'].values,
    )

    if st.button("Recommend"):
        with st.spinner('Fetching recommendations...'):
            names, posters = recommend(selected_movies_name)

            cols = st.columns(5)

            for idx, col in enumerate(cols):
                with col:
                    st.text(names[idx])
                    st.image(posters[idx])