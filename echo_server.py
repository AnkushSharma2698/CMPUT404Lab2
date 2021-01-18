#!/usr/bin/env python3
import socket
import os

HOST = 'localhost'
PORT = 8001
HEADER = 10

child_pid = os.getpid()
def echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            connection, address = s.accept() # This is blocking
            print("Connector: ", address)
            child_pid = os.fork() # When a request is received, fork the program
            if child_pid == 0: # In the child process
                with connection:
                    # This loop runs as long as the data being sent is
                    while True:
                        data = connection.recv(2048)
                        msg = f'{len(data):<{HEADER}}'+ data.decode('utf-8')
                        print(data)
                        if not data:
                            break
                        connection.send(bytes(msg, 'utf-8'))
                    s.close()
                    break
            else: # In the parent process
                # We do not want the main process dealing with open connections, that simply delegates
                # to other processes
                connection.close()
                    


if __name__ == "__main__":
    echo_server()