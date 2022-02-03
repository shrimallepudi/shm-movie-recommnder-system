import streamlit as st
import pickle
import requests

st.title('Movie Recommender System')

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
selected_movie = st.selectbox('Select the movie you like, from the list:', movies['title'])

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2013cfb6e806cdfbf15198fba5229273')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    five_similar_movies = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for sim in five_similar_movies:
        movie_id = movies.iloc[sim[0]].id
        recommended_movies.append(movies.iloc[sim[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    col0, col1, col2, col3, col4 = st.columns(5)
    with col0:
        st.image(posters[0])
        st.write(names[0])
    with col1:
        st.image(posters[1])
        st.write(names[1])
    with col2:
        st.image(posters[2])
        st.write(names[2])
    with col3:
        st.image(posters[3])
        st.write(names[3])
    with col4:
        st.image(posters[4])
        st.write(names[4])