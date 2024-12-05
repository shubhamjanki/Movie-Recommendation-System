import pickle
import streamlit as st
import requests

# Function to fetch the movie poster using OMDb API
def fetch_poster(movie_name):
    API_KEY = "38e69448"  # Your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True' and 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"  # Placeholder image

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(fetch_poster(movie_name))
    return recommended_movie_names, recommended_movie_posters

# Streamlit app setup
# App title
st.markdown(
    """
    <div style=" white-space: nowrap; width:900px">
        <h1 style="color: #e50914; font-family: 'Arial', sans-serif; font-weight: bold;">
        🎥 Movie Recommender System
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)


# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for selecting a movie
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
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
