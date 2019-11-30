#!/usr/bin/env python3
#Christina Gaglio
#Fall 2019
#use Tweepy to open a connection to the Twitter streaming api to continuously pull tweets

import pandas as pd
import csv

import tweepy
from tweepy.api import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#open a connection
#resp = self.session.request('POST', url, data=self.body,timeout=self.timeout, stream=True, auth=auth, verify=self.verify)

#consumer key
TWITTER_APP_KEY= 'WP3jnTWxycVuVQT0gBujAi3XOr1grT0eK0gQKgOAlv5jG'
#consumer Secret
TWITTER_APP_SECRET='WsYpQaVZFwyQCKm4aesis6yFo'

#access token
TWITTER_KEY= '1184608278266953728-4BUFm0Pr6x5f9BTeHPXlIWpaJc6yjb'
#access token secret
TWITTER_SECRET= 'WP3jnTWxycVuVQT0gBujAi3XOr1grT0eK0gQKgOAlv5jG'

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

api = tweepy.API(auth)


#set up the listener
#on_status: create a listener that only takes the text of the tweet
#on_error: disconnects if twitter sends a 420 error code indicating the program reached its limit of tweets it can pull
class StreamListener(tweepy.StreamListener):
	tweet_text=[]
	tweet_user=[]
	def on_status(self, status):
		#we can filter to remove a tweet if it was retweeted
		#if status.retweeted_status:
			#return
		
		tweet_text.append(status.text)
		tweet_user.append(status.user.screen_name)
		df=pd.Dataframe({'text':tweet_text, 'user':tweet_user})
		#print the text from the tweet
		print(status.text)	
		print(df)
	
		export_csv=df.to_csv('streamTweets.csv', index=None, header=True)
	def on_error(self, status_code):
		if status_code==420:
			return False

#start the listener
#this will stream tweets of the topic indicated in the filer
stream_listener= StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["#Frozen 2", "#TheGame"])
