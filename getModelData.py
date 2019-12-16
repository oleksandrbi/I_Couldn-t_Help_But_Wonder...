import pandas as pd
from sqlMethods import *

def main():
    con = getConnection()
    sql = """
        SELECT
            raw_tweets.tweet_id,
            raw_tweets.tweet_text,
            clean_tweets.clean_text,
            manual_tweet_sentiments.sentiment,
            manual_tweet_sentiments.relevant
        FROM
            raw_tweets
                JOIN
            clean_tweets ON raw_tweets.tweet_id = clean_tweets.tweet_id
                JOIN
            manual_tweet_sentiments ON raw_tweets.tweet_id = manual_tweet_sentiments.tweet_id
    """

    data = execute(con,sql)
    df = pd.DataFrame(data)
    df.to_csv('sentimented_tweets.csv')

main()
