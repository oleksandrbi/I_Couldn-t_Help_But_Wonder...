#For Yuliang to use to build Server

from sqlMethods import *
import urllib.parse
#this method returns ALL restaurants we want to classify, filtering out based on criteria (that we haven't set yet)
#This doesn't filter out rest's already classified
def getRestaurants(con):
    restaurants = selectAll(con, 'restaurant_data')

    toClassify = list()
    #Alex : write some code to filter these based on smth we decide
    #If its simpler, I can return objs that just have Rest Name and ID
    for rest in restaurants:
        if(True):
            toClassify.append(rest)
    return toClassify


#INPUT : Restaurant object
#OUTPUT :STRING location search query(for DB), String of URL of Location Search
def getTwitterLocSearchURL(rest):
    loc = str(rest['latitude']) + ',' + str(rest['longitude']) + ',.5km'
    url = 'https://twitter.com/search?q=' + urllib.parse.quote('lang:en geocode:' + loc)
    return loc, url
