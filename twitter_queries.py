#!/usr/bin/env python3
#Christina Gaglio
#Fall 2019
#use Twitter Api to open a connection to the Twitter streaming api to continuously pull tweets

import pandas as pd
import csv
import sys
import pymysql
import tweepy

from sqlMethods import addTweets,getConnection
from authTwitter2 import authTW




def get_queries():
	mydb = getConnection()
	cursor = mydb.cursor()
	#executes this sql statement - get the queries when the type is a query
	cursor.execute("SELECT twitter_query, restaurant_id FROM twitter_queries WHERE query_type='QUERY'")
	queries = cursor.fetchall()

	q=[]
	i=[]
	for x in queries:
		q.append(x['twitter_query'])
		i.append(x['restaurant_id'])

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
	newTweets = []
	while r<len(topics.index):
		q=topics.iloc[r]['query']
		count=100
		#check if q has any text
		if (q.strip() != ''):
			# use the twitter api to get the tweets

			search_results = t_obj.search.tweets( q = q, count = count,tweet_mode='extended')
			# filter the json results just to status
			statuses = search_results['statuses']
		 	#Collect List of New IDS or instead
			tweets = addTweets(con, statuses,q,topics.iloc[r]['rest_id'])
			newTweets.extend(tweets)
		r+=1
	return newTweets

def main():
	t_obj=authTW()
	get_tweets(t_obj)
#main()
