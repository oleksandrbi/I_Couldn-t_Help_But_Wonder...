#Christina Gaglio
#Fall 2019
#Retrive yelp reviews of restaurents specially those in name.csv.
#This pulls 3 reviews per restaurant

import pandas as pd
import csv
import json
import requests


#open csv  of resturants in a pandas dataframe
#save restaurant id for review retrival
#save restaurtant name for funsies (possible use later)
df= pd.read_csv('Names.csv')
rest_id= df.iloc[:,1]
rest_name= df.iloc[:,0]

#make a request for restaurant reviews using the yelp API
#need api key
api_key = 'bpXuHXEvrbDopIV1xnDamTrDq4eU906oLZbzk1C4gcSKMjULNebsyrpHQf0ajKQ6cSYGVfv_YNYgY0CfkZtdD05UCMdqO67vwwk9NqL3mV7IXDYzhJ2-oPSzLaDNXXYx'
headers = {'Authorization': 'Bearer %s' % api_key}

#should give back 60 reviews (3 per restaurant)
i=0
while i<len(rest_id):
	rest=rest_id[i]
	url= 'https://api.yelp.com/v3/businesses/%s/reviews' % rest
	params={'term':' Restaurant','location':'Las Vagas'}

	req=requests.get(url,params,headers=headers)

	parsed=json.loads(req.text)
	reviews=parsed["reviews"]

	#uncomment at your own risk, will take a minute to output
        #prints review id, reviewer profile, reviewer url, review text, review url...
	#print(json.dumps(parsed, indent=4))
	i=i+1


