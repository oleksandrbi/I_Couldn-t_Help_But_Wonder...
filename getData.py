#Oleksandr Bihary
#Using Zomato API we obtain resturants names in the Las Vegas area and their Reviews
#API KEY: aa2e170fced5e4de42b96789a76fbd7f

import zomatopy

config = { "user_key":"aa2e170fced5e4de42b96789a76fbd7f" }
city_name = "Las Vegas"

zomato = zomatopy.initialize_app(config)

#Getting ID for a particular city
city_ID = zomato.get_city_ID(city_name)

#Getting the cuisines in a city
cuisine_dictionary = get_cuisines(city_ID)

#Getting all establishment types in a city.
establishment_types_dictionary = get_establishment_types(city_ID)

#Getting the details of a particular restaurant
restaurant_details = get_restaurant(restaurant_ID)
