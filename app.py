recommended_movies = recommend(option)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for idx, movie_name in enumerate(recommended_movies):
        poster_url = get_movie_poster(movie_name)
        with [col1, col2, col3, col4, col5][idx]:
            if poster_url:
                st.image(poster_url, width=150)
            st.write(f"🎥 **{movie_name}**")
