# !/usr/bin/env python


import numpy as np
import pandas as pd



movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')





movies = movies.merge(credits,on='title')



movies = movies[['movie_id','revenue','popularity','vote_average','vote_count','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)


def convert(l):
    req=[]
    for i in eval(l):
        req.append(i['name'])
    return req


movies['keywords'] = movies['keywords'].apply(convert)
movies['genres'] = movies['genres'].apply(convert)





def convert3characters(l):
    req=[]
    count=0
    for i in eval(l):
        if(count>3):
            break
        req.append(i['character'])
        count+=1
    
    return req
    

movies['characters'] = movies['cast'].apply(convert3characters)


def convert3names(l):
    req=[]
    count=0
    for i in eval(l):
        if(count>3):
            break
        req.append(i['name'])
        count+=1
    
    return req

movies['cast'] = movies['cast'].apply(convert3names)


def get_director(l):
    req=[]
    for i in eval(l):
        if i['job'] == 'Director':
            req.append(i['name'])
            break
    return req


movies['crew'] = movies['crew'].apply(get_director)



movies['overview'] = movies['overview'].apply(lambda x: x.split())



movies['overview'] = movies['overview'].apply(lambda x: [i.replace(" ","") for i in x])


movies['overview'].apply(lambda x:[i for i in x if i!=""])

movies['characters'] = movies['characters'].apply(lambda x: [i.replace(" ","") for i in x])


movies['tags'] = movies['overview'] +movies['keywords']+ movies['genres'] + movies['cast'] + movies['characters'] + movies['crew']


movies.head()




new_df = movies[['movie_id','title','tags','popularity','revenue','vote_count','vote_average']]



new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())


new_df['genres'] = movies['genres']




from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


vectors = cv.fit_transform(new_df['tags']).toarray()

import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


def stem(text):
    y=[]
    
    for i in text.split():
        y.append(ps.stem(i))
    
    return " ".join(y)
    
new_df['tags'] = new_df['tags'].apply(stem)
new_df = new_df.sort_values(by=['popularity'],ascending=False)


new_df = new_df.drop_duplicates(subset=['title'])




from sklearn.metrics.pairwise import cosine_similarity


similarity = cosine_similarity(vectors)


def recommend(movie_title):
       movie_index = new_df[new_df['title'] == movie_title].index[0]
       similarities = similarity[movie_index]
       movies_list = sorted(list(enumerate(similarities)),reverse=True,key = lambda x: x[1])[1:6]
       
       for i in movies_list:
           print(new_df.iloc[i[0]].title)


import pickle

pickle.dump(new_df,open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
