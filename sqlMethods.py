#Alex Kaish
#Fall 2019
#Methods to access, update, and read from the sql database

import pymysql
from datetime import datetime
from dateutil.parser import parse


#method to get connection to sql database
#make SURE at the end of each method that deals with this you call connection.close()
def getConnection():
    connection = pymysql.connect(host='10.22.12.131',
                                 user='root',
                                 password='SCL$Xdat4ML',
                                 db='Wonder',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

#Execute a SQL Command, Return values if any selected
#Commit: If true, will commit changes
def execute(con,sql,commit=False):
    #Check to make sure con is still active
    if not con.open:
        print("Connection to SQL Server has been dropped. Attempting to reconnect")
        max_attempts = 10
        trynum = 0
        while not con.open and trynum < max_attempts:
            con.ping(reconnect=True)


    print("Executing :", sql)
    with con:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        if(commit):
            con.commit()
        return rows

#Selects and returns all columns and rows from table
def selectAll(con, table,extra=None):
    with con:
        if(extra == None):
            sql = "SELECT * FROM %s"%(table)
        else:
            sql = "SELECT * FROM %s %s"%(table, extra)
        rows = execute(con,sql)
        return rows


#Adds Data to SQL Database
#data is {column : value}
#if IgnoreDuplicates, Will Ignore when duplicate Primary Key, not change table
#If updateDuplicate, Will update all values when duplicate Primary Key
#if not, will throw error when duplicate Primary Key encounted, Should only be used when you're chcecking if duplciate rroe
def insert(con,table, data,commit,ignoreDuplicates=True,updateDuplicates=False):
    if(updateDuplicates):
        ignoreDuplicates = False
        #updateDuplicate overrides ignoreDuplicates, because they cannot be run concurrently
        #Replace works exactly the same as Insert except for updating functions
        sql = "REPLACE INTO %s (%s) VALUES (%s)"
    elif(ignoreDuplicates):
        sql = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s=%s"
    else:
        sql = "INSERT INTO %s (%s) VALUES (%s)"
    #Create string of columns
    cols = ""
    for col in data.keys():
        cols = cols + col + ","
    cols = cols[:-1]
    #Create string of values
    values = ""
    for val in data.values():
        #con.escape adds quotes, escapes escape chars, converts datetime/bool/others, doesn't work on dicts
        #escapedVal is val but in format valid for SQL
        if type(val) == dict:
            escapedVal = con.escape(str(val))
        else:
            escapedVal = con.escape(val)
        values = values + escapedVal + ","
    values = values[:-1]
    if(ignoreDuplicates):
        #end of str is 'UPDATE col=col', where col is any existing val, works to ignore
        sql = sql%(table,cols,values,list(data)[0],list(data)[0])
    else:
        sql = sql%(table,cols,values)
    execute(con, sql, commit)

def insertAll(con,table, allData,ignoreDuplicates=True,updateDuplicates=False):
    for data in allData:
        insert(con,table, data,False,ignoreDuplicates=ignoreDuplicates,updateDuplicates=updateDuplicates)
    con.commit()

#This Section is yelp
def addYelpRestaurants(con,restaurants):
    insertAll(con, 'restaurant_data', restaurants)

def addYelpReviews(con,reviews):
    insertAll(con, 'yelp_reviews', reviews)


#All Below are methods for Tweets

#Add a list of tweets from a python twitter search
#All twitter calls must have tweet_mode='extended'
def addTweets(con,tweets,query,restaurant_id):
    added = []
    for tweet in tweets:
        tw = addTweet(con,tweet,query,restaurant_id,False)
        added.append(tw)
    con.commit()
    return added



#Adds a Tweet and its user, and all  entities within it (hashtags, user mentions, and urls)to the databases
#tweet is python twitter tweet
#All twitter calls must have tweet_mode='extended'
def addTweet(con,tweet,query, restaurant_id, commit):

    #These are all Indented b/c they are only called from AddTweet
    #Adds user to the twitter_users table
    #only call from addTweet
    def addUser(con, userData,commit):
        data = {
        'user_id' : userData['id'],
        'full_name' : userData['name'],
        'username' : userData['screen_name'],
        'follower_count' : userData['followers_count'],
        'verified' : userData['verified'],
        'statuses_count' : userData['statuses_count']
        }
        insert(con, 'twitter_users',data,commit)

    #Only call from addTweet
    def parseEntities(con, tweet,tweet_id, commit):
        #start stop index are [)
        #These are double indented to run from parseEntities
        #only call from addTweet
        def addHashtag(con, hashtagData,tweet_id,commit):
            data = {
                'tweet_id' : tweet_id,
                'entity_type' : 'HASHTAG',
                'start_index' : hashtagData['indices'][0],
                'stop_index' : hashtagData['indices'][1],
                'text' : hashtagData['text']
            }
            insert(con,'tweet_entities',data,commit)

        #only Call from Addtweet
        def addURL(con, urlData,tweet_id,commit):
            data = {
                'tweet_id' : tweet_id,
                'entity_type' : 'URL',
                'url' : urlData['url'],
                'display_url'  : urlData['display_url'],
                'expanded_url' : urlData['expanded_url'],
                'start_index' : urlData['indices'][0],
                'stop_index' : urlData['indices'][1]
            }
            insert(con,'tweet_entities',data,commit)

        #Only Call from AddTweet
        def addUserMention(con,userMenData,tweet_id,commit):
            data = {
                'tweet_id' : tweet_id,
                'entity_type' : 'USER_MENTION',
                'start_index' : userMenData['indices'][0],
                'stop_index' : userMenData['indices'][1],
                'user_id' : userMenData['id'],
                'username' : userMenData['screen_name'],
                'full_name' :userMenData['name']
                }
            insert(con,'tweet_entities',data,commit)

        def addMedia(con,mediaData, tweet_id,commit):
            data = {
                'tweet_id' : tweet_id,
                'entity_type' : 'MEDIA',
                'url' : mediaData['url'],
                'display_url'  : mediaData['display_url'],
                'expanded_url' : mediaData['expanded_url'],
                'start_index' : mediaData['indices'][0],
                'stop_index' : mediaData['indices'][1]
            }
            insert(con,'tweet_entities',data,commit)

        entities = tweet['entities']
        for hashtag in entities['hashtags']:
            addHashtag(con,hashtag,tweet_id,commit)
        for url in entities['urls']:
            addURL(con,url,tweet_id,commit)
        for mention in entities['user_mentions']:
            addUserMention(con,mention,tweet_id,commit)
        if('extended_entities' in tweet):
            for media in tweet['extended_entities']['media']:
                addMedia(con,media,tweet_id,commit)

    #addTweet Method Begins
    twData = tweet
    data = {
    'tweet_id' : twData['id'],
    'tweet_text' : twData['full_text'],
    'retweet_count' : twData['retweet_count'],
    'favorite_count' : twData['favorite_count'],
    #Stores time as dateTime
    'timestamp' : parse(twData['created_at']),
    'user_id' : twData['user']['id'],
    'twitter_query' : query,
    'restaurant_id' : restaurant_id,
    'twitter_client' : twData['source']
    }
    #deal with if quoted tweet
    if(twData['is_quote_status']):
        data['quoted_tweet_id'] = twData['quoted_status_id']
    #deals with retweet
    #We can pull in orig tweet if ppl like that
    if('retweeted_status' in twData):
        data['retweeted_tweet_id'] = twData['retweeted_status']['id']
    if('in_reply_to_status_id' in twData):
        data['reply_to_tweet_id'] = twData['in_reply_to_status_id']
    insert(con, 'raw_tweets',data, commit)

    #Parse user
    addUser(con,twData['user'],commit)
    #Parse Entities
    parseEntities(con,twData,twData['id'],commit)
    return data
