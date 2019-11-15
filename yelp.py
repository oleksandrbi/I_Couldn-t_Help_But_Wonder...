#Christina Gaglio
#Fall 2019
#Pull restaurtant names,address, and ratings using the Yelp API

import requests
import json
import pandas as pd
import csv

def get_datarequest():
	api_key = 'bpXuHXEvrbDopIV1xnDamTrDq4eU906oLZbzk1C4gcSKMjULNebsyrpHQf0ajKQ6cSYGVfv_YNYgY0CfkZtdD05UCMdqO67vwwk9NqL3mV7IXDYzhJ2-oPSzLaDNXXYx'
	headers = {'Authorization': 'Bearer %s' % api_key}

	url = 'https://api.yelp.com/v3/businesses/search'
	params = {'term':'Restaurants','location':'Las Vagas'}

	req=requests.get(url,params,headers=headers)
	return req	

	#print('The status code is {}'.format(req.status_code))


def get_name():
	req=get_datarequest()

	#convert the data to a JSON object
	parsed=json.loads(req.text)
#print the json data gathered from the GET request
#this data includes, rest name, url, review count, rating, price range, location(city, zip, and street address), phone number) 
	#print(json.dumps(parsed, indent=4))


#extract data from the json file
#keep some info in a Dataframe: name address and rating
#name ,add, rating, to add to a dataframe
	name=[]
	business_id=[]
	address=[]
	rating=[]
	latitude=[]
	longitude=[]
	businesses = parsed["businesses"]
	for business in businesses: 
		#print("Name:", business["name"])
		#print("Address:", " ".join(business["location"]["display_address"]))
		#print("Rating:", business["rating"])
		#print("Coordinates: ", business["coordinates"]["latitude"])
	
		name.append(business["name"])
		business_id.append(business["id"])
		rating.append(business["rating"])
		address.append(business["location"]["display_address"])	
		latitude.append(business["coordinates"]["latitude"])
		longitude.append(business["coordinates"]["longitude"])

	df=pd.DataFrame({'Name': name,'ID':business_id,'Address': address,'Latitude': latitude, 'Longitude':longitude,'rating':rating})
	print(df.head())
	print(df.shape)
	#export the data to a csv file
	export_csv=df.to_csv('Names.csv',index=None,header=True)
	return df

def main():
#	get_request()
	get_name()
#	get_reviews(df)
main()










