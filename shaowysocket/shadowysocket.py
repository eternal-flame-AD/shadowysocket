import socket
import asyncio


class shadowysocket():
    def __init__(self, conn: socket.socket):
        self.conn=conn
    
    def send(self, data):
        return self.conn.send(data)
    
    def sendall(self, data):
        return self.conn.sendall(data)
    
    def recv(self, bufsize):
        return self.conn.recv(bufsize)
    
    def recvfrom(self, bufsize):
        return self.conn.recvfrom(bufsize)
    
    def setblocking(self, flag:bool):
        self.conn.setblocking(flag)
    
    def settimeout(self, timeout):
        self.conn.settimeout(timeout)