import os
import sys


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(parentdir)
sys.path.insert(0, parentdir)

import threading
import socket
import asyncio

import shadowysocket

class echoserver():
    
    def __init__(self):
        self.conn = socket.socket()
        self.conn.bind(("127.0.0.1",12300))
        self.conn.listen()
        while True:
            conn, address = self.conn.accept()
            conn = shadowysocket.shadowysocket(conn)
            threading.Thread(target=self.echo,args=(conn, address)).start()
    
    def echo(self, conn, address):
        data = conn.recv(4096)
        conn.sendall(data + address[0].encode('utf-8'))

class echoclient():

    def __init__(self):
        self.conn = socket.create_connection(("127.0.0.1", 12300))
        self.conn = shadowysocket.shadowysocket(self.conn)
    
    def send(self, data):
        self.conn.sendall(data)
    
    def recv(self):
        return self.conn.recv(4096)

def test_socket():
    server = threading.Thread(target=echoserver)
    server.daemon = True
    server.start()
    client = echoclient()
    client.send(b"hello world")
    assert client.recv() == b"hello world127.0.0.1"
    
