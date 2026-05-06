import json
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other import *
from error import InputError
#from backend.common import mysql_operate
from common import mysql_operate
from flask import jsonify
from datetime import datetime
from common.mysql_pool import db
import movie as movi
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def movie_detail(id,token):
    """
    get the detail of the movie for both logged in and logged out user
    :param id: the id of the movie
    :param token: the token of the user(if available or ''))
    :return: {
        'movie': detail of the movie,
        'wish': the number of user who added the movie to the wishlist,
        'watched': the number of user who added the movie to the watchedlist,
        'diector': the director information of the movie,
        'star': the star information of the movie,
        'review': the review information of the movie,`
        'movie_u_may_like': the list of other movie the user who liked this movie also liked
        'recommendation': the list of other movie the user may like
    }
    
    pre-condition: the movie_id is valid and the movie has been added to the database
    error: InputError - the movie_id is invalid
    """
    sql = "select * from movie_tbl where movie_id = ('%s')" %(id)
    data = list(db.execute_query(sql))  
    # get the director of the movie
    sql = "select * from direct_in_tbl where movie_id = ('%s')" %(id)
    director = list(db.execute_query(sql))
    directorlist = []
    for dir in director:
        sql = "select * from director_tbl where director_id = ('%s')" %(dir['director_id'])
        directorlist.append(list(db.execute_query(sql))[0])
    # get the star of the movie
    sql = "select * from star_in_tbl where movie_id = ('%s')" %(id)
    star = list(db.execute_query(sql))
    starlist = []
    for sta in star:
        sql = "select * from star_tbl where star_id = ('%s')" %(sta['star_id'])
        starlist.append(list(db.execute_query(sql))[0])
    # get the number of user who added the movie to the wishlist
    sql = "select * from movie_wishlist_tbl where movie_id = ('%s')" %(id)
    wish = list(db.execute_query(sql))
    numWish = len(wish)
    # get the number of user who added the movie to the watchedlist
    sql = "select * from movie_watchlist_tbl where movie_id = ('%s')" %(id)
    watched = list(db.execute_query(sql))
    numWatched = len(watched)
    # get the number of reviews
    data = movi.movie_num_review_single(data[0])
    # update the number of views
    sql = "UPDATE movie_tbl SET movie_views = movie_views + 1 WHERE movie_id = '{}'".format(id)
    db.execute_query(sql)
    # get the movie you may like (get the list of other movie the user who liked this movie also liked)
    u_may_like = movie_u_may_like(id)
    # check if the user has added the movie to the wishlist or watchedlist
    if token == '':
        # for logged out user
        # get the review of the movie
        sql = "select * from movie_review_tbl where movie_id = ('%s')" %(id)
        review = list(db.execute_query(sql))
        for rev in review:
            rev['permission'] = False
            # add user's name and phote to the review
            sql = "select * from user_tbl where user_id = ('%s')" %(rev['user_id'])
            user = list(db.execute_query(sql))[0]
            rev['user_name'] = user['user_name']
            rev['user_profile_photo'] = user['user_profile_photo']
        # recommendation
        recommendation = movie_recommendation(data, 5)
        #recommendation = movie_num_review(recommendation, 'numReview')
        
        return {
            'movie': data,
            'wish': False,
            'watched': False,
            'director': directorlist,
            'star': starlist,
            'numWish': numWish,
            'numWatched': numWatched,
            'review': review,
            'recommendation': recommendation,
            'movie_u_may_like': u_may_like
        }
    else:
        # for logged in user
        # check if the token is valid
        sql = "SELECT * FROM token_tbl"
        store = list(db.execute_query(sql))
        check_valid_token(token, store)
        # decode the token, get the user's id
        input_dict = decode_jwt(token)
        auth_user_id = input_dict['u_id']
        sql = "SELECT * FROM movie_wishlist_tbl where user_id = ('%s') and movie_id = ('%s')" %(auth_user_id, id)
        store = list(db.execute_query(sql))
        wish = False
        watched = False
        if len(store) != 0:
            wish = True
        sql = "SELECT * FROM movie_watchlist_tbl where user_id = ('%s') and movie_id = ('%s')" %(auth_user_id, id)
        store = list(db.execute_query(sql))
        if len(store) != 0:
            watched = True
        # delete the blacklist's review
        sql = "select * from movie_review_tbl where movie_id = ('%s')" %(id)
        review = list(db.execute_query(sql))
        for rev in review:
            sql = "select * from user_blacklist_tbl where black_id = ('%s')" %(rev['user_id'])
            black = list(db.execute_query(sql))
            for bla in black:
                if bla['user_id'] == auth_user_id:
                    review.remove(rev)
        # check if the user has permission to see the review
        for rev in review:
            # add user's name and phote to the review
            sql = "select * from user_tbl where user_id = ('%s')" %(rev['user_id'])
            user = list(db.execute_query(sql))[0]
            rev['user_name'] = user['user_name']
            rev['user_profile_photo'] = user['user_profile_photo']
            rev['tag'] = user['user_tag']
            if rev['user_id'] == auth_user_id:
                rev['permission'] = True
            else:
                sql = "select * from user_tbl where user_id = ('%s')" %(auth_user_id)
                user = list(db.execute_query(sql))
                if user[0]['user_permission'] == 'admin':
                    rev['permission'] = True
                else:
                    rev['permission'] = False
        
        recommendation = movie_recommendation_with_token(data, auth_user_id)
        #recommendation = movie_num_review(recommendation, 'numReview')
        return {
            'movie': data,
            'wish': wish,
            'watched': watched,
            'director': directorlist,
            'star': starlist,
            'numWish': numWish,
            'numWatched': numWatched,
            'review': review,
            'recommendation': recommendation,
            'movie_u_may_like': u_may_like
        }

def movie_search(word, pages, sortBy):
    """
    Search the movie by name, director, star, and can sort by rating, review number, release date, views, best match, and name
    :param word: the word you want to search
    :param pages: the page you want to see
    :param sortBy: the way you want to sort the result
    :return: the list of movie

    pre-condition: word is a string, pages is an integer, sortBy is a string
    """
    word_clean = re.sub(r'-?"[^"]*"', "", word)
    word_clean = re.sub(r"-?\'[^\']*\'", "", word_clean)
    # search the movie by name
    sql = "select * from movie_tbl where movie_name like '%{}%'".format(word_clean)
    data = list(db.execute_query(sql))  
    
    # search the movie by director
    sql = "select * from direct_in_tbl where director_id in (select director_id from director_tbl where director_name like '%{}%')".format(word_clean)
    dir_in = list(db.execute_query(sql))
    for dir in dir_in:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(dir['movie_id'])
        data.append(list(db.execute_query(sql))[0])
    # search the movie by star
    sql = "select * from star_in_tbl where star_id in (select star_id from star_tbl where star_name like '%{}%')".format(word_clean)
    star_in = list(db.execute_query(sql))
    for star in star_in:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(star['movie_id'])
        data.append(list(db.execute_query(sql))[0])
    # search the movie by type
    sql = "select * from movie_tbl where movie_tag like '%{}%'".format(word_clean)
    type_in = list(db.execute_query(sql))
    data = data + type_in
    # remove the duplicate
    new_list = []
    for item in data:
        if item not in new_list:
            new_list.append(item)
    data = new_list
    #print(word_clean)
    # deal with the inclusive and exclusive
    if extract_text2(word) != []:
        for i in extract_text2(word):
            for j in data:
                if i in j['movie_name']:
                        data.remove(j)
                    
    word = re.sub(r"-\'([^\']*)\'", "", word)
    word = re.sub(r"-\"([^\"]*)\"", "", word)
    if extract_text(word) != []:
        for i in extract_text(word):
            for j in data:
                if i not in j['movie_name']:
                    data.remove(j)
    
    pages = pages - 1
    data = sort_movie_list(data, sortBy)
    
    return {
        'movies': data[5 * pages: 5 * pages + 5],
        'numPages': len(data) // 5 + 1
    }

# helper function
# get the number of review for each movie in a list
def movie_num_review(movie_list, name):
    # add number of review
    for movie in movie_list:
        sql = "select * from movie_review_tbl where movie_id = ('%s')" %(movie['movie_id'])
        data = list(db.execute_query(sql))
        movie[name] = len(data)
    return movie_list

# helper function
# get the number of review for pitcular movie
def movie_num_review_single(movie):
    # get movie review number
    sql = "select * from movie_review_tbl where movie_id = ('%s')" %(movie['movie_id'])
    movie['numOfReviews'] = len(list(db.execute_query(sql)))
    return movie

# helper function
# data management for movie detail page and movie recommendation
def movie_recommendation(mov, result_num):
    movies = pd.read_excel('resource/Movie.xlsx')
    movies = movies.fillna("NULL")
    """movies = pd.read_excel('resource/Movie_INFO.xlsx')
    # join dirctor and star from director_in_tbl and star_in_tbl
    dir = pd.read_excel('resource/Direct_IN_INFO.xlsx')
    star = pd.read_excel('resource/Star_IN_INFO.xlsx')
    dir = dir[['moveie_id', 'director_id', 'director_name']]
    star = star[['moveie_id', 'star_id', 'star_name']]
    movies = pd.merge(movies, dir, on='moveie_id')
    movies = pd.merge(movies, star, on='moveie_id')
    # group by movie_id and join director name and star name
    movies['director_name'] = movies['director_name'].astype(str)
    movies['star_name'] = movies['star_name'].astype(str)
    movies['moveie_id'] = movies['moveie_id'].astype(int)
    movies = movies.groupby('moveie_name').agg({'moveie_id': 'first', 'moveie_name': 'first', 'movie_tag': 'first', 'director_name': ', '.join, 'star_name': ', '.join})
    movies = movies.reset_index(drop=True)
    # save the movie as file
    movies.to_excel('resource/Movie.xlsx', index=False)"""
    result = get_similar_movies(movies, mov['movie_id'], result_num).to_dict('records')
    for movie in result:
        sql = "select * from movie_tbl where movie_id = ('%s')" %(movie['movie_id'])
        data = list(db.execute_query(sql))
        movie['movie_rating'] = data[0]['movie_rating']
        movie['movie_cover'] = data[0]['movie_cover']
        movie = movie_num_review_single(movie)
    return result

# helper function
# get the similar movies considering the user information
def movie_recommendation_with_token(mov, user_id):
    result = movie_recommendation(mov, 20)
    # delete the movie that user has watched or wishced or reviewed
    sql = "select * from movie_review_tbl where user_id = ('%s')" %(user_id)
    review = list(db.execute_query(sql))
    sql = "select * from movie_wishlist_tbl where user_id = ('%s')" %(user_id)
    wish = list(db.execute_query(sql))
    sql = "select * from movie_watchlist_tbl where user_id = ('%s')" %(user_id)
    watched = list(db.execute_query(sql))
    sql = "select * from movie_review_tbl where user_id = ('%s')" %(user_id)
    review = list(db.execute_query(sql))
    for movie in result:
        for w in wish:
            if movie['movie_id'] == w['movie_id']  and (movie in result):
                result.remove(movie)
        for w in watched:
            if movie['movie_id'] == w['movie_id'] and (movie in result):
                result.remove(movie)
        for w in review:
            if movie['movie_id'] == w['movie_id'] and (movie in result):
                result.remove(movie)
        for w in review:
            if movie['movie_id'] == w['movie_id'] and (movie in result):
                result.remove(movie)
    return result[:5]

# helper function
# get the similar movies by algorithm
def get_similar_movies(df, movie_id, N):
    # Check if the movie_id exists in the DataFrame
    if movie_id not in df['movie_id'].values:
        print(f"{movie_id} does not exist in the DataFrame.")
        return pd.DataFrame()

    # Initialize the count vectorizer
    vectorizer = CountVectorizer()

    # Fit and transform the movie tag, director, and star columns
    X = vectorizer.fit_transform(df['movie_tag'].fillna('') + ' ' + df['director_name'].fillna('') + ' ' + df['star_name'].fillna(''))

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(X)

    # Get the index of the movie with the given movie_id
    idx = df[df['movie_id'] == movie_id].index[0]

    # Get the pairwise similarity scores between the given movie and all other movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on their similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top N similar movies
    sim_indices = [i for i, s in sim_scores[1:N+1]]

    # Return the top N similar movies as a new DataFrame
    return df.iloc[sim_indices]

# helper function
# get the movie that other user like this movie also like
def movie_u_may_like(movie_id):
    # return a list of top rating movie in the wishlist of the user has added this movie the wishlist
    sql = "select * from movie_wishlist_tbl where movie_id = ('%s')" %(movie_id)
    data = list(db.execute_query(sql))
    result = []
    if len(data) == 0:
        sql = "select * from movie_tbl order by movie_rating desc"
        movie2 = list(db.execute_query(sql))
        for mov in movie2:
            mov = movi.movie_num_review_single(mov)
        return movie2[:5]
    else:
        for user in data:
            sql = "select * from movie_wishlist_tbl where user_id = ('%s')" %(user['user_id'])
            wish = list(db.execute_query(sql))
            for movie in wish:
                sql = "select * from movie_tbl where movie_id = ('%s')" %(movie['movie_id'])
                movie = list(db.execute_query(sql))
                movie[0] = movi.movie_num_review_single(movie[0])
                if movie[0] not in result:
                    result.append(movie[0])
        result = sorted(result, key=lambda x: x['movie_rating'], reverse=True)
        if len(result) < 5:
            # add top rating movie if the number of movie is less than 5
            sql = "select * from movie_tbl order by movie_rating desc"
            data = list(db.execute_query(sql))
            for mov in data:
                mov = movi.movie_num_review_single(mov)
            result.append(data[:5-len(result)])
        return result[:5]

# helper function
# Extracts the text inside double quotes from a given string.
def extract_text(text):
    return re.findall(r'"([^"]*)"', text) + re.findall(r'\'([^\']*)\'', text)

def extract_text2(text):
    return  re.findall(r"-\'([^\']*)\'", text) + re.findall(r'-"([^"]*)"', text)

# helper function
# help for sorting the movie list
def sort_movie_list(data, sortBy):
    # add number of review to the movie
    data = movie_num_review(data, 'numReview')
    
    # deal with the dirty data
    for c in data:
        if c['movie_name'] == 'NULL':
            c['movie_name'] = 'Unknown'
        if c['movie_release_date'] == 'NULL':
            c['movie_release_date'] = '0'
    # sort the result
    if sortBy == 'Rating: High to Low':
        data = sorted(data, key=lambda x: x['movie_rating'], reverse=True)
    elif sortBy == 'Rating: Low to High':
        data = sorted(data, key=lambda x: x['movie_rating'], reverse=False)
    elif sortBy == 'Review: More to Less':
        data = sorted(data, key=lambda x: x['numReview'], reverse=True)
    elif sortBy == 'Review: Less to More':
        data = sorted(data, key=lambda x: x['numReview'], reverse=False)
    elif sortBy == 'Release: New to Old':
        data = sorted(data, key=lambda x: x['movie_release_date'], reverse=True)
    elif sortBy == 'Release: Old to New':
        data = sorted(data, key=lambda x: x['movie_release_date'], reverse=False)
    elif sortBy == 'Name: Z to A':
        data = sorted(data, key=lambda x: x['movie_name'], reverse=True)
    elif sortBy == 'Name: A to Z':
        data = sorted(data, key=lambda x: x['movie_name'],reverse=False)
    elif sortBy == "Views: More to Less":
        data = sorted(data, key=lambda x: x['movie_views'], reverse=True)
    elif sortBy == "Views: Less to More":
        data = sorted(data, key=lambda x: x['movie_views'], reverse=False)
    # elif sortBy == 'BestMatch':
    return data