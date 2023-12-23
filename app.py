import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    try:
        index = movies_list[movies_list['title'] == movie].index.tolist()[0]
        distance = similarity[index]
        predict = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
        recommended = []
        recommended_movies_poster = []
        for j in predict:
            movie_id = movies_list.iloc[j[0]]['id']
            # fetch from API
            recommended.append(movies_list.iloc[j[0]]['title'])
            recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended,recommended_movies_poster
    except IndexError:
        return ["Movie not found or unable to make recommendations"]


# Load data
movies_list = pickle.load(open('movies.pkl', 'rb'))
if isinstance(movies_list, pd.DataFrame):
    movies_list = movies_list.reset_index(drop=True)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', movies_list['title'])
if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
