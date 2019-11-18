import socket, threading
import sys

corpus = ['Comment 1', 'Comment 2', 'Comment 3', 'Comment 4']

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
                for x in corpus:
                    dx = x.encode('ASCII')
                    self.csocket.send(dx)
                    label = self.csocket.recv(1024)
                    print(label)

                    #store label into database
                    sys.stdout.flush()
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
