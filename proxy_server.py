#!/usr/bin/env python3
import socket
import os

HOST = 'localhost'
PORT = 8003
# Consideration: Is it worth sending header data of msg size? To eliminate client while loop
# And set the buffer size before recieving? This might be inefficient if the message is HUGE :(


# Proxy only works for like 3 requests, not exactly sure why
def proxy_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ps:
            
            ps.bind((HOST, PORT)) # Bind Proxy Server to Specified host and port
            ps.listen() # Begin listening at the bound address
            while True:
                connection, address = ps.accept() # Block and begin accepting incoming connections
                print("Connected Client Address: ", address)
                child_pid = os.fork()
                if child_pid == 0:
                    # Create socket to field messages to google
                    google_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    google_socket.connect(("www.google.com", 80))

                    # Get data from the client
                    conn_data = receive_message(connection)

                    # Send data to google
                    google_socket.sendall(conn_data) 

                    # Recieve response from google
                    proxy_data = receive_message(google_socket, 4096)

                    # Send data back to client
                    connection.sendall(proxy_data) 

                    # Close all socket connections for the child process
                    connection.close()
                    google_socket.close()
                    ps.close()
                    break            
                else:
                    # Do not want to do anything with the primary process connection
                    connection.close()


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