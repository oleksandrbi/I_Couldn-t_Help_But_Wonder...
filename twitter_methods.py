from sqlMethods import *
import pandas as pd
from twitter_queries import *

def get_all_entities(con):
    sql = """
            SELECT
                tweet_id, entity_type, start_index, stop_index
            FROM
                tweet_entities
            WHERE
                entity_type = 'USER_MENTION'
                    OR entity_type = 'URL'
                    OR entity_type = 'MEDIA'
            ORDER BY stop_index
    """
    data = execute(con, sql)
    df = pd.DataFrame(data).drop_duplicates()
    return df

#clean an individual tweet
def clean_tweet(tw,entitiesDf):
    tweet_id = tw['tweet_id']
    raw_text = tw['tweet_text'].lower()
    #clean entities
    entities = entitiesDf[entitiesDf['tweet_id'] == tweet_id]
    amt = entities.shape[0]
    #Check if there are any entiries
    if(amt == 0):
        clean = raw_text
    else:
        clean = ""
        startInd = 0
        for entitityId in entities.index[:-1]:
            entity = entities.loc[entitityId]
            clean += raw_text[startInd:entity['start_index']]
            startInd = entity['stop_index']
        clean += raw_text[startInd:entities.iloc[-1]['start_index']]
        clean += raw_text[entities.iloc[-1]['stop_index']:]

    #clean query
    query = tw['twitter_query'].lower()
    clean = clean.replace(query,"")
    print()
    print("QUERY : ", query)
    print('ORIG : ', raw_text)
    print('CLEAN: ',clean )
    return clean

#if nothing passed in for newTweets, clean ALL tweets
def clean_tweets(con,newTweets = []):
    entitiesDf = get_all_entities(con)
    if(len(newTweets) == 0):
        #Pull all tweets from DB
        raw_tweets = selectAll(con,'raw_tweets')
    else:
        #Tweets passed in
        raw_tweets = newTweets
    clean_tweets = []
    for tw in raw_tweets:
        clean = clean_tweet(tw,entitiesDf)
        dbObj = {
        'tweet_id' : tw['tweet_id'],
        'clean_text' : clean
        }
        clean_tweets.append(dbObj)
    insertAll(con,'clean_tweets',clean_tweets,updateDuplicates=True)
    return clean_tweets

def getTweetsAndClean():
    con = getConnection()
    t_obj=authTW()
    tweets = get_tweets(t_obj)
    clean = clean_tweets(con,tweets)
    con.close()
    return clean

def main():
    getTweetsAndClean()
    #t_obj=authTW()
    #get_tweets(t_obj) #rename to load tweets
    #Classify New tweets
    #do node stuff





if __name__ == '__main__':
    main()
