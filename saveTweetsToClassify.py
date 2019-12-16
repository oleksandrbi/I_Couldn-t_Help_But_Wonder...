import pandas as pd
from sqlMethods import *


def make_smaller_df(df):
    pass
    #for loop basically divide by # in csv, then push

def main():

    con = getConnection()

    sql = """
    SELECT raw_tweets.tweet_id, raw_tweets.tweet_text, clean_tweets.clean_text
    FROM raw_tweets
    JOIN clean_tweets
    ON
    raw_tweets.tweet_id=clean_tweets.tweet_id
    """
    dbData = execute(con, sql)

    df = pd.DataFrame(dbData)


    df.to_csv('tweets.csv')

main()
