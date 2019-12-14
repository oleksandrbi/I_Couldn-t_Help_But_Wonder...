import socket
import select

HOST = '10.22.12.224'
PORT = 65432

def newUI(info):
    print()
    print(info)
    print()
    locResp = input("Were the tweets from that URl relevant? Enter y or n :")
    while(locResp != 'y' and locResp != 'n'):
        locResp = input("That was not a valid answer, please entere either y or n : ")
    if (locResp == 'y'):
        print("you inputed yes")
        locBool = 1
        print(locBool)
    else:
        print("you entered no")
        locBool = 0
    queries = input("Please enter other Valid twitter queries for this restaurant, seperated by commas: ")
    if queries == '':
        queries = 'NONE'
    #put in code to verify that queries are in correct format, figure out a correct format
    return locBool, queries
    #send THIS info back to the Server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    #Identification
    s.send(b'yx')
    s.settimeout(5)

    running = True
    while(running):
        data = s.recv(1024)
        #Change to Str?
        datas = data.decode('utf-8')
        bool, query = newUI(datas)
        querys = query.encode('utf-8')
        s.send(bool.to_bytes(2, 'little'))
        s.send(querys)
