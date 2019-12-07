import socket, threading
import sys
import pymysql

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
        sql = "SELECT * FROM %s"%(table)
        rows = execute(con,sql)
        return rows


con = getConnection()
sql = "SELECT review_id, review_text FROM yelp_reviews"
corpus = execute(con, sql)

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
                
            for x in corpus:
                t_context = x['review_text']
                t_id = x['review_id']
                dx = t_context.encode('ASCII')
                self.csocket.send(dx)
                label = self.csocket.recv(1024)
                stored_value = "('" + u_id + "', '" + t_id + "', '" + label.decode("utf-8") + "');"
                sql = "INSERT INTO raw_manual_tweet_sentiments (client_id, tweet_id, sentiment) VALUES " + stored_value
                print(sql)
                sys.stdout.flush()
                execute(con, sql)

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
