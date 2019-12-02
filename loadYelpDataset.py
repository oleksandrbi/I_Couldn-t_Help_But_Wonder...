#!/usr/bin/env python3
# Author : Oleksandr Bihary and Alex Kaish
# Date   : Nov 25 2019
# Description   : opens yelp dataset with business and gives user all the business in Vegas area, then it filters out the revies by resturant ID, loads into DB
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

import json
import pandas as pd
from sqlMethods import *


BUZZfilePATH = r'/home/admin/Downloads/YelpData/business.json'
REVfilePATH = r'/home/admin/Downloads/YelpData/review.json'

def main():
    #ALL STUFF TO GET VEGAS BUSINESS
    # open input file:
    print("FILTERING BUSINESSES")
    Bfile = open(BUZZfilePATH, encoding="utf8")
    all_data = list()
    for i, line in enumerate(Bfile):
        # convert the json on this line to a dict
        data = json.loads(line)
        # extract what we want
        dbObj = {}
        dbObj['restaurant_id'] = data['business_id']
        dbObj['restaurant_name'] = data['name']
        dbObj['address'] = data['address']
        dbObj['city'] = data['city']
        dbObj['state'] = data['state']
        dbObj['postal_code'] = data['postal_code']
        dbObj['latitude'] = data['latitude']
        dbObj['longitude'] = data['longitude']
        dbObj['avg_yelp_rating'] = data['stars']
        dbObj['review_count'] = data['review_count']
        dbObj['attributes'] = data['attributes']
        dbObj['categories']= data['categories']
        dbObj['hours'] = data['hours']

        isRestaurant = (dbObj['categories'] is not None) and ("Restaurants" in data['categories'].split(','))
        # add to the data collected so far, filtering for only Open Restaurants in Las Vegas
        if (dbObj['city'] == "Las Vegas") and (data['is_open'] != 0) and (isRestaurant):
            all_data.append(dbObj)


    # create the DataFrame
    yelpData = pd.DataFrame(all_data)
    #Get Restaurant IDs to get REVIEWS
    restIds = yelpData['restaurant_id']
    yelpData.to_csv('./yelpDATASET/vegasBUZZ.csv')
    print("BUSINESS")
    print(yelpData)
    Bfile.close()
    print("LOADING BUSINESSES INTO DB")
    #Load into database
    con = getConnection()
    addYelpRestaurants(con,all_data)

    print("PROCESSING REVIEWS")
    #ALL STUFF TO GET VEGAS REVIEWS
    # open input file:
    Rfile = open(REVfilePATH, encoding="utf8")
    all_data = list()
    for i, line in enumerate(Rfile):
        # convert the json on this line to a dict
        data = json.loads(line)
        #Check if review correlates to the Restarants in Vegas
        if (data['business_id'] in restIds.values):
            dbObj = {}
            # extract what we want
            dbObj['review_id'] = data['review_id']
            dbObj['restaurant_id'] = data['business_id']
            dbObj['user_id'] = data['user_id']
            dbObj['rating'] = data['stars']
            dbObj['review_text'] = data['text']
            dbObj['timestamp'] = data['date']
            #Make sure this works
            dbObj['useful'] = data['useful']
            dbObj['funny'] = data['funny']
            dbObj['cool'] = data['cool']
            all_data.append(dbObj)


    # create the DataFrame
    df = pd.DataFrame(all_data)
    df.to_csv('./yelpDATASET/vegasREV.csv')
    print("REVIEWS")
    print(df)
    Rfile.close()
    #add to Database
    print("LOADING REVIEWS INTO DB")
    addYelpReviews(con,all_data)
    con.close()



if __name__ == '__main__':
    main()
