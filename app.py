import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def search(query):
    matches=[]
    for tag in movies['tags']:
        count=0
        for word in query.split(" "):
            if word.lower() in tag:
                count+=1
        matches.append(count)
    
    matches = sorted(list(enumerate(matches)),reverse=True,key= lambda x : x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in matches[0:5]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    count = 0
    for i in distances[1:]:

        if count > 5:
            break

        movie_index = i[0]
        if selected_genre!='' and selected_genre not in movies.iloc[movie_index]['genres']:
            continue

        

        count+=1

        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommendations')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Liked a movie? Get similar recommendations",
    movie_list
)
st.write('OR')

genres = ['Romance','Action','Science Fiction','Adventure','Fantasy','Family','Animation','Comedy','Drama','Mystery','Thriller','History','War']

selected_genre = st.selectbox(
    "Search by Genre",
    genres
)
st.write('OR')

search_query = st.text_input('Search by keywords')

if st.button('Show Recommendations'):
    columns = st.columns(5)

    if(search_query==''):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        for i in range(min(5,len(recommended_movie_names))):
            with columns[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

    else:
        recommended_movie_names,recommended_movie_posters = search(search_query)
        for i in range(min(5,len(recommended_movie_names))):
            with columns[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])


