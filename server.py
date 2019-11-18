import socket
import sys

HOST = '127.0.0.1'
PORT = 65432

corpus = ['Comment 1', 'Comment 2', 'Comment 3', 'Comment 4']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            datas = data.decode('ASCII')
            if datas == 'yx':
                for x in corpus:
                    dx = x.encode('ASCII')
                    conn.send(dx)
                    label = conn.recv(1024)
                    print(label)
                    sys.stdout.flush()
