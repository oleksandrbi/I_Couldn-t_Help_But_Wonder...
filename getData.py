#Oleksandr Bihary
#Using Zomato API we obtain resturants names in the Las Vegas area and their Reviews
#API KEY: aa2e170fced5e4de42b96789a76fbd7f

import requests
from pprint import pprint


locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/cities?lat=28&lon=77"
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "aa2e170fced5e4de42b96789a76fbd7f"}

response = requests.get(locationUrlFromLatLong, headers=header)

pprint(response.json())

