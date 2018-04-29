import os
import sys
import threading
import socket
import time


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import shadowysocket


class echoserver():

    def __init__(self):
        self.conn = socket.socket()
        self.conn.bind(("127.0.0.1", 12300))
        self.conn.listen(5)
        while True:
            conn, address = self.conn.accept()
            conn = shadowysocket.shadowysocket(conn)
            threading.Thread(target=self.echo, args=(conn, address)).start()

    def echo(self, conn, address):
        while True:
            data = conn.recv(4096)
            if len(data) == 0:
                break  # connection close
            conn.sendall(data + address[0].encode('utf-8'))


class echoclient():

    def __init__(self):
        self.conn = socket.create_connection(("127.0.0.1", 12300))
        self.conn = shadowysocket.shadowysocket(self.conn)

    def send(self, data):
        self.conn.sendall(data)

    def recv(self):
        return self.conn.recv(4096)

    def close(self):
        self.conn.close()


def test_socket():
    server = threading.Thread(target=echoserver)
    server.daemon = True
    server.start()
    for _ in range(3):
        client1 = echoclient()
        client2 = echoclient()
        client1.send(b"hello world")
        assert client1.recv() == b"hello world127.0.0.1"
        client2.send(b"another client")
        assert client2.recv() == b"another client127.0.0.1"
        client1.send(b"bye")
        assert client1.recv() == b"bye127.0.0.1"
        client1.close()
        client2.close()
    time.sleep(0.5)  # wait for connection thread to die
    assert threading.active_count() == 2  # main+server


if __name__ == "__main__":
    test_socket()
