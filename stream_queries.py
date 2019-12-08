#!/usr/bin/env python3
#Christina Gaglio
#Fall 2019
#use Tweepy to open a connection to the Twitter streaming api to continuously pull tweets

import pandas as pd
import csv
import sys
import tweepy

from tweepy.api import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from sqlMethods import *

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

def get_queries(con):

	#executes this sql statement - get the queries when the type is a query
	#does not work with locations
	queries = execute(con,"SELECT twitter_query,restaurant_id FROM twitter_queries WHERE query_type='QUERY'")
	return queries

#set up the listener
#on_status: create a listener that only takes the text of the tweet
#on_error: disconnects if twitter sends a 420 error code indicating the program reached its limit of tweets it can pull
class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		#print the text from the tweet
		print(status.text)

		#we can filter to remove a tweet if it was retweeted
		#if status.retweeted_status:
			#return

	def on_error(self, status_code):
		print(status_code)

def main():
	#start the listener
	#this will stream tweets of the topic indicated in the filer
	stream_listener= StreamListener()
	stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
	#establish a connection to the sql database
	con = getConnection()
	#get the keywords (hashtags) that the stream should pull about the restaurtant from twitter_queries table in database using the get_queries function
	rest_track=get_queries(con)
	stream.filter(track=rest_track)
	stream.flush()
	#Closes Connection to the SQL Database
	con.close()

main()
