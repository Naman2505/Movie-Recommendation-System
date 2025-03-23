import streamlit as st
import pandas as pd
import pickle as pk
import os
import requests

# 🟢 TMDB API Setup
API_KEY = "ec836886034e22e92c733a37fc4b3e31"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# ✅ Function to Fetch Movie Poster
def get_movie_poster(movie_name):
    movie_id = movies_list[movies_list["title"] == movie_name]["id"].values
    if len(movie_id) == 0:
        return None  # Return None if poster is unavailable
    
    movie_id = movie_id[0]
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return IMAGE_BASE_URL + poster_path
    return None  # Return None if no poster is found

# ✅ Movie Recommendation Function
def recommend(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]  # Get top 5
    
    recommended_movies = [movies_list.iloc[i[0]].title for i in movie_list]
    return recommended_movies  # Returns titles only

# ✅ Load Data
file_path = "movies.pkl"
similarity_path = "similarity.pkl"

if os.path.exists(file_path) and os.path.exists(similarity_path):
    # movies_list = pk.load(open(file_path, "rb"))
    # similarity = pk.load(open(similarity_path, 'rb'))
    movies_list = pd.read_pickle(file_path)
    similarity = pd.read_pickle(similarity_path)
else:
    st.error("🛑 Required files (movies.pkl / similarity.pkl) not found!")
    st.stop()

# ✅ Check if Data Loaded
if isinstance(movies_list, pd.DataFrame):
    if "id" not in movies_list.columns:
        st.error("🛑 'movies.pkl' is missing the 'id' column. Please update your dataset!")
        st.stop()
    else:
        movies_names = movies_list["title"].values  # Extract movie titles
else:
    st.error("movies.pkl does not contain a DataFrame!")
    st.stop()

# 🔥 Streamlit UI
st.title("🎬 Movie Recommendation System")

option = st.selectbox("🔍 Select a Movie", movies_names)

if st.button("🔎 Search"):
    st.write("🎯 **Top 5 Recommended Movies:**")

    # 🔵 Create 5 Columns for Display
    col1, col2, col3, col4, col5 = st.columns(5)
    
    recommended_movies = recommend(option)
    
    for idx, movie_name in enumerate(recommended_movies):
        poster_url = get_movie_poster(movie_name)
        
        # Assign each movie to the correct column
        with [col1, col2, col3, col4, col5][idx]:  
            if poster_url:
                st.image(poster_url, width=150)
            st.write(f"🎥 **{movie_name}**")
