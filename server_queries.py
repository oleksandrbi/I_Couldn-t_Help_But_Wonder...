import socket, threading
import sys
import pymysql
import pandas as pd
import urllib.parse
from sqlMethods import *


#gets query to Store in DB
def getTwitterLocQuery(rest):
    loc = str(rest['latitude']) + ',' + str(rest['longitude']) + ',.5km'
    return loc

#Gets url to show to show in program
def getTwitterLocSearchURL(rest):
    url = 'https://twitter.com/search?q=' + urllib.parse.quote('lang:en geocode:' + getTwitterLocQuery(rest))
    return url

def getMessage(rest):
    info ='Your next restaurant is : \n' + rest['restaurant_name'] + '\n'+  rest['address'] + '\n' + rest['city'] + ', ' +rest['state'] + ' ' + str(rest['postal_code']) + '\n The url to search for tweets at this location is : \n' + getTwitterLocSearchURL(rest)
    return info

def addQueries(con,restID,locBool, locText,queries):
    if (locBool):
        locQuery = {'twitter_query' : locText,
        'query_type' : 'LOCATION',
        'restaurant_id' : restID }
        insert(con,'twitter_queries',locQuery,False)
    for queryText in queries:
        query = {'twitter_query' : queryText,
        'query_type' : 'QUERY',
        'restaurant_id' : restID }
        insert(con,'twitter_queries',query,False)
    #Updates Restaurnt Entry in DB
    sql = "UPDATE restaurant_data SET queries_set='1' WHERE restaurant_id='%s'"%restID;
    execute(con,sql)
    con.commit()

def getRestFromDB(con):
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
            LIMIT 100
        """
    corpus = execute(con, sql)
    df = pd.DataFrame(corpus)
    df.set_index('restaurant_id',inplace = True)
    df['active'] = 0 #used to make sure no one works on the same Restaurant at the same time
    return df

def getNextRestaurant():
    toClassify =  df[(df['active'] == 0) & (df['queries_set'] == 0)]
    if (toClassify.size > 0):
        return toClassify.iloc[0]
    else:
        print("Ran out of Restaurants, start the program again")
        con.close()
        exit()
        #Tony idk if this is good but I couldn't figure out how to reload into the same df from the function

#Begin Program
con = getConnection()
df = getRestFromDB(con)

#Thread to handle socket connection from client
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection from: ", clientAddress)
    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(1024)
            if not data:
                break
            datas = data.decode('ASCII')
            if datas == 'yx':
                u_id = '1'
            elif datas == 'alexk':
                u_id = '2'
            elif datas == 'alexb':
                u_id = '3'
            elif datas == 'cg':
                u_id = '4'
            elif datas == 'ricky':
                u_id = '5'
            #Maybe figure out how to ask "Do you want to continue? in the client and send that responce"
            while(True):
                rest = getNextRestaurant()
                r_id = rest.name
                #mark as active so not sent to a diff user
                df.at[r_id,'active'] = 1
                r_message = getMessage(rest)
                r_loc = getTwitterLocQuery(rest)

                #need to send : restInfo
                dx = r_message.encode('ASCII')
                self.csocket.send(dx)
                bool = self.csocket.recv(1024)
                q = self.csocket.recv(1024)

                intB = int.from_bytes(bool, byteorder='little')
                if (intB == 1):
                    locationBool = True
                else:
                    locationBool = False

                print("test")
                print(intB)
                print(locationBool)
                print(q)
                sys.stdout.flush()
                #Need to recieve "location boolean, other queries"

                #test Data, Delete Below
                queries = []
                queries.append(rest['restaurant_name'])
                #test Data, Delete Above

                addQueries(con,r_id,locationBool,r_loc,queries)

                sys.stdout.flush()
                #Set that it is done in local df
                df.at[r_id,'active'] = 0
                df.at[r_id,'queries_set'] = 1

        print ("Client at ", clientAddress , " disconnected...")

LOCALHOST = "127.0.0.1"
PORT = 65432

#declaring server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
