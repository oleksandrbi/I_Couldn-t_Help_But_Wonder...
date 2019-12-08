import socket, threading
import sys
import pymysql
import pandas as pd
import urllib.parse


def getConnection():
    connection = pymysql.connect(host='10.22.12.131',
                                 user='root',
                                 password='SCL$Xdat4ML',
                                 db='Wonder',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def execute(con,sql,commit=False):
    print("Executing :", sql)
    with con:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        if(commit):
            con.commit()
        return rows

def selectAll(con, table):
    with con:
        sql = "SELECT * FROM %s LIMIT 10"%(table)
        rows = execute(con,sql)
        return rows

#gets query to Store in DB
def getTwitterLocQuery(rest):
    loc = str(rest['latitude']) + ',' + str(rest['longitude']) + ',.5km'
    return loc

#Gets url to show to show in program
def getTwitterLocSearchURL(rest):
    url = 'https://twitter.com/search?q=' + urllib.parse.quote('lang:en geocode:' + getTwitterLocQuery(rest))
    return url


def getMessage(rest):

    info ='Your next restaurant is : \n' + rest['restaurant_name'] +  rest['address'] + '\n' + rest['city'] + ', ' +rest['state'] + ' ' + str(rest['postal_code']) + '\n The url to search for tweets at this location is : \n' + getTwitterLocSearchURL(rest)
    return info

def addQueries(con,restID,locBool, locQuery,queries):
    #I'll code this later tn or tmmrw
    pass

con = getConnection()
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
df['active'] = 0 #used to make sure no one works on the same program at the same time

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
            #Is there a way to update this every time the foro loop runs, Tony ignore this problem I'll fix it
            for r_id in df[(df['active'] == 0) & (df['queries_set'] == 0)].index:
                rest = df.loc[r_id]
                #mark as active so not sent to a diff user
                df.at[r_id,'active'] = 1
                r_message = getMessage(rest)
                r_loc = getTwitterLocQuery(rest)

                #need to send : restInfo
                dx = r_message.encode('ASCII')
                self.csocket.send(dx)
                label = self.csocket.recv(1024)
                #Need to recieve "location boolean, other queries"

                addQueries(con,id,locationBool,r_loc,queries)

                stored_value = "('" + u_id + "', '" + t_id + "', '" + label.decode("utf-8") + "');"
                sql = "INSERT INTO raw_manual_tweet_sentiments (client_id, tweet_id, sentiment) VALUES " + stored_value
                print(sql)
                sys.stdout.flush()
                execute(con, sql)
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
