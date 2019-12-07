#For Yuliang to use to build Server

from sqlMethods import *
import urllib.parse
import pandas as pd

#this method returns ALL restaurants we want to classify, filtering out Already Classified Restaurants and prioritizing ones with the most review in the past year
def getRestaurants(con):
    sql = """
        SELECT
            restaurant_data.*,
            COUNT(yelp_reviews.review_id) AS num_recent_reviews
        FROM
            yelp_reviews
                JOIN
            restaurant_data ON yelp_reviews.restaurant_id = restaurant_data.restaurant_id
        WHERE
            timestamp >= '2017-11-14 18:06:13'
                AND queries_set = 0
        GROUP BY restaurant_id
        ORDER BY num_recent_reviews DESC
    """
    restaurants =  execute(con,sql)
    return restaurants

#INPUT : Restaurant object
#OUTPUT :STRING location search query(for DB), String of URL of Location Search
def getTwitterLocSearchURL(rest):
    loc = str(rest['latitude']) + ',' + str(rest['longitude']) + ',.5km'
    url = 'https://twitter.com/search?q=' + urllib.parse.quote('lang:en geocode:' + loc)
    return loc, url
