#Oleksandr Bihary
#Using Zomato API we obtain resturants names in the Las Vegas area and their Reviews
#API KEY: aa2e170fced5e4de42b96789a76fbd7f

import pprint
from pyzomato import Pyzomato
pp = pprint.PrettyPrinter(indent=2)

p = Pyzomato("aa2e170fced5e4de42b96789a76fbd7f")
p.search(q="las vegas")

categories = p.getCategories()
pp.pprint( categories )

dets = p.getCollectionsViaCityId(282)
pp.pprint( dets )

cus = p.getCuisines(282)
pp.pprint( cus )

estab = p.getEstablishments(282)
pp.pprint( estab )

#need resturant ID
menu = p.getDailyMenu(292)
pp.pprint( menu )

#need resturant ID
info = p.getRestaurantDetails(292)
pp.pprint( info )

#need resturant ID
reviews = p.getRestaurantReviews(291)
pp.pprint( reviews )