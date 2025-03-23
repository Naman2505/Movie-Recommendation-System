import streamlit as st
import pandas as pd
import pickle as pk
import os
import gdown  # ✅ Google Drive Downloader

# ✅ Google Drive File IDs
MOVIES_FILE_ID = "1ck5Q4EU8jqadShFaEzqjlwiEJYNqM1je"
SIMILARITY_FILE_ID = "1Bmqjg5XHyPtd4sSjo1wPRq-82v0eZgQx"

# ✅ Function to Download `.pkl` Files using gdown
def download_from_drive(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

# ✅ File Paths
movies_path = "movies.pkl"
similarity_path = "similarity.pkl"

# ✅ Download Files if Not Present
if not os.path.exists(movies_path):
    st.warning("📥 Downloading `movies.pkl` from Google Drive...")
    download_from_drive(MOVIES_FILE_ID, movies_path)

if not os.path.exists(similarity_path):
    st.warning("📥 Downloading `similarity.pkl` from Google Drive...")
    download_from_drive(SIMILARITY_FILE_ID, similarity_path)

# ✅ Load Data
try:
    movies_list = pd.read_pickle(movies_path)
    similarity = pd.read_pickle(similarity_path)
except Exception as e:
    st.error(f"🛑 Error loading `.pkl` files: {e}")
    st.stop()

# ✅ Validate Data
if isinstance(movies_list, pd.DataFrame) and "title" in movies_list.columns:
    movies_names = movies_list["title"].values
else:
    st.error("🛑 `movies.pkl` does not contain a valid DataFrame!")
    st.stop()

# 🔥 Streamlit UI
st.title("🎬 Movie Recommendation System")

option = st.selectbox("🔍 Select a Movie", movies_names)

if st.button("🔎 Search"):
    st.write("🎯 **Top 5 Recommended Movies:**")
    recommended_movies = recommend(option)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for idx, movie_name in enumerate(recommended_movies):
        poster_url = get_movie_poster(movie_name)
        with [col1, col2, col3, col4, col5][idx]:
            if poster_url:
                st.image(poster_url, width=150)
            st.write(f"🎥 **{movie_name}**")

