import pickle
import streamlit as st
import pandas as pd
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set title and sidebar
st.title('Movie Recommendetion System - Anik Chowdhury Project')
st.sidebar.title('User Input')

# Select movie from sidebar
selected_movie_name = st.sidebar.selectbox(
    'Select your movie',
    movies['title'].values)

# Button to display recommended movies
if st.sidebar.button('Get Recommendations'):
    recommendations, posters = recommend(selected_movie_name)
    st.markdown("## Recommended Movies:")
    col1, col2, col3, col4, col5 = st.columns(5)  # Create columns for each poster
    for i in range(len(recommendations)):
        col = [col1, col2, col3, col4, col5][i]
        col.image(posters[i], caption=recommendations[i], width=100)
        col.write(recommendations[i])

# Add some style using markdown
st.sidebar.markdown('---')
st.sidebar.markdown('**About this App:**')
st.sidebar.markdown('This app recommends similar movies based on the movie you select.')

# Add footer with additional information
st.sidebar.markdown('---')
st.sidebar.markdown(
    """
    *This app is created by Anik Chowdhury as a project.*  
    *For educational purposes only.*  
    *Source code available on [GitHub](https://github.com/anikchowdhury91/movie-recommender-system).*  
    """
)
