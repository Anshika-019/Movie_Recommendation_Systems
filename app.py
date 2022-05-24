from typing import List, Any

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=66e5b07a9a8ab2044b19e01c7ea274cf&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

rows = 3
cols = 4
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: rows * cols + 1]

    names = []
    posters = []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id
           #fetch the movie Poster
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    names = np.array(names).reshape(rows, cols)
    posters = np.array(posters).reshape(rows, cols)
    return names,posters


movies_dict= pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    for row in range(rows):
        gride = st.columns(cols)
        for col in range(cols):
            with gride[col]:
                st.text(names[row][col])
                st.image(posters[row][col])
