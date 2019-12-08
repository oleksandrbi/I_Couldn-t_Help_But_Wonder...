import socket
import select

HOST = '127.0.0.1'
PORT = 65432

def newUI(info):
    print()
    print(info)
    print()
    locResp = input("Were the tweets from that URl relevant? Enter y or n :")
    #Put in code to verify that answer was y or n
    if (locResp == 'y'):
        locBool = True
    else:
        locBool = False
    queries = input("Please enter other Valid twitter queries for this restaurant : ")
    #put in code to verify that queries are in correct format, figure out a correct format
    return locBool, queries
    #send THIS info back to the Server

def ui(s, label):
    if label == 'y':
        print('sending y')
        s.send(b'POS')
    elif label == 'n':
        print('sending n')
        s.send(b'NEG')
    elif label == 'exit':
        running = False
    else:
        print("Wrong format of input, Please enter y for yes, n for no. exit for closing this program")
        rl = input()
        ui(s, rl)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    #Identification
    s.send(b'yx')
    s.settimeout(5)

    running = True
    while(running):
        data = s.recv(1024)
        print('Received', repr(data))
        label = input()
        ui(s, label)
