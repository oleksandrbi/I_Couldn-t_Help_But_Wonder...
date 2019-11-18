import socket
import select

HOST = '127.0.0.1'
PORT = 65432

def ui(s, label):
    if label == 'y':
        print('sending y')
        s.send(b'y')
    elif label == 'n':
        print('sending n')
        s.send(b'n')
    elif label == 'exit':
        running = False
    else:
        print("Wrong format of input, Please enter y for yes, n for no. exit for closing this program")
        rl = input()
        ui(s, rl)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b'yx')
    s.settimeout(5)

    running = True
    while(running):
        data = s.recv(1024)
        print('Received', repr(data))
        label = input()
        ui(s, label)
