#!/usr/bin/env python3
#Christina Gaglio
#Fall 2019
#use Tweepy to open a connection to the Twitter streaming api to continuously pull tweets

import pandas as pd
import csv
import sys
import pymysql
import tweepy

from sqlMethods import addTweets
from authTwitter2 import authTW
from tweepy.api import API
from tweepy import OAuthHandler

def twitter_auth():
	#consumer key
	TWITTER_APP_KEY= 'WsYpQaVZFwyQCKm4aesis6yFo'
	#consumer Secret
	TWITTER_APP_SECRET= 'eUcuO9u7fz6YIB2M0RYHhu9m9WzNMrK7dlOxWGhCZCfgk3kXmS'

	#access token
	TWITTER_KEY= '1184608278266953728-4BUFm0Pr6x5f9BTeHPXlIWpaJc6yjb'
	#access token secret
	TWITTER_SECRET= 'WP3jnTWxycVuVQT0gBujAi3XOr1grT0eK0gQKgOAlv5jG'

	auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
	auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

	api = tweepy.API(auth)
	return api

#establish a connection to the database
def getConnection():
	return  pymysql.connect(host = '10.22.12.131', 
				user = 'root',
				password='SCL$Xdat4ML',
				database='Wonder', )

def get_queries():
	mydb = getConnection()
	cursor = mydb.cursor()
	#executes this sql statement - get the queries when the type is a query 
	cursor.execute("SELECT twitter_query, restaurant_id FROM twitter_queries WHERE query_type='QUERY'")
	queries = cursor.fetchall()

	q=[]
	i=[]
	for x in queries:
		q.append(x[0])
		i.append(x[1])

	df=pd.DataFrame({'query':q, 'rest_id':i})
#	cursor.execute("SELECT twitter_qyery FROM twitter_queries WHERE query_type='LOCATION'")
#	loc_queries = curosr.fetchall()
#	loc=[]
#	for x in loc_queries:
#		loc.append(x)
#	return loc
	return df 

def get_tweets(t_obj):
	topics=get_queries()
	con=getConnection()
	r=0
	while r<len(topics.index):
		q=topics.iloc[r]['query']
		count=100
		# use the twitter api to get the tweets
		search_results = t_obj.search.tweets( q = q, count = count,tweet_mode='extended')
		# filter the json results just to status
		statuses = search_results['statuses']

#		addTweets(con, statuses,q,topics.iloc[r]['rest_id'])

		r+=1

def main():
	t_obj=authTW()
	get_tweets(t_obj)
main()
