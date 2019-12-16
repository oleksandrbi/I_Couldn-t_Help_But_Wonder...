#Alex Kaish
#Load in classified sentiments from csv

from sqlMethods import *
import pandas as pd


def main():
    con = getConnection()
    df = pd.read_csv('classified_tweets.csv',header=1,usecols=['tweet_id','tweet_text', 'clean_text', 'sentiment','relevant'],index_col = 'tweet_id')
    df.fillna(1,inplace=True)
    forDb = []
    for tweet_id in df.index:
        tw = df.loc[tweet_id]
        dbObj = {
        'tweet_id' : tweet_id,
        'sentiment' : int(tw['sentiment']),
        'relevant' : int(tw['relevant'])
        }
        forDb.append(dbObj)
    insertAll(con, 'manual_tweet_sentiments',forDb)
    con.close()

main()
