#!/usr/bin/env python3
import socket
import os
from multiprocessing import Process

HOST = 'localhost'
PORT = 8003
# Consideration: Is it worth sending header data of msg size? To eliminate client while loop
# And set the buffer size before recieving? This might be inefficient if the message is HUGE :(
remote_host = "www.google.com"
remote_port = 80

# Proxy only works for like 3 requests, not exactly sure why
def proxy_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ps:
            ps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ps.bind((HOST, PORT)) # Bind Proxy Server to Specified host and port
            ps.listen() # Begin listening at the bound address
            while True:
                connection, address = ps.accept() # Block and begin accepting incoming connections
                print("Connected Client Address: ", address)
                 # Create socket to field messages to google
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_sock:
                     remote_sock.connect((remote_host, remote_port))
                     p = Process(target=handle_request, args =(connection, address, remote_sock))
                     p.daemon = True
                     p.start()
                     print("Process started: ", p)
                connection.close() # Close connection for the parent process

def handle_request(conn, addr, remote_sock):
    msg = receive_message(conn, 4096)
    remote_sock.sendall(msg) # Send message to google
    remote_sock.shutdown(socket.SHUT_WR) # No more writing
    remote_msg = receive_message(remote_sock, 4096)
    print("sending message back to client")
    conn.sendall(remote_msg)

# Pass in a socket that is current connected
# Pass in buffer size, although default should be okay
def receive_message(sock, buf_size=1024):
    sock.settimeout(0.3) # Timeout is set to deal with blocking nature of socket.recv
    msg = b""
    while True:
        try:
            data = sock.recv(buf_size)
            if not data:
                break
        except socket.error as e:
            break
        else:
            msg += data
    return msg


if __name__ == "__main__":
    proxy_server()