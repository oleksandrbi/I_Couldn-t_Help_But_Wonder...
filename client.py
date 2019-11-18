import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b'yx')

    running = True
    while(running):
        data = s.recv(1024)
        print('Received', repr(data))
        label = input()
        if label == 'y':
            print('sending y')
            s.send(b'y')
        elif label == 'n':
            print('sending n')
            s.send(b'n')
        elif label == 'exit':
            running = False
        else: print("Wrong format of input")
