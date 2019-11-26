#!/usr/bin/env python3
# Author : Oleksandr Bihary
# Date   : Nov 25 2019
# Description   : opens yelp dataset with business and gives user all the business in Vegas area, then it filters out the revies by resturant ID
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

import json
import pandas as pd

filePATH = 'C:\\Users\\obiha\\Desktop\\yelp_dataset\\business.json'

# open input file: 
ifile = open(filePATH, encoding="utf8") 
stop = 192574
all_data = list()
for i, line in enumerate(ifile):  
    # convert the json on this line to a dict
    data = json.loads(line)
    # extract what we want
    business_id = data['business_id']
    name = data['name']
    address = data['address']
    city = data['city']
    state = data['state']
    postal_code = data['postal_code']
    latitude = data['latitude']
    longitude = data['longitude']
    stars = data['stars']
    review_count = data['review_count']
    is_open = data['is_open']
    attributes = data['attributes']
    categories = data['categories']
    hours = data['hours']

    # add to the data collected so far
    if (city == "Las Vegas"):
        all_data.append([business_id,name,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open,attributes,categories,hours])

# create the DataFrame
df = pd.DataFrame(all_data, columns=['business_id','name','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','attributes','categories','hours'])
df.to_csv('vegas.csv')
print(df)
ifile.close()
