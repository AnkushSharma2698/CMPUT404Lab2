#!/usr/bin/env python3
import socket
import os

HOST = 'localhost'
PORT = 8001
HEADER = 10

child_pid = os.getpid()
def echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        while True:
            connection, address = s.accept() # This is blocking
            print("Connector: ", address)
            data = connection.recv(4096)
            connection.sendall(data)
            connection.close()
            


if __name__ == "__main__":
    echo_server()
