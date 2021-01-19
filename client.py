#!/usr/bin/env python3
import socket
import sys

def client():
    # utilizing context manager so no need to call s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = 'www.google.com'
        s.connect((host , 80)) # Connect to google on port 80
        payload = "GET / HTTP/1.0\r\nHost: {host}\r\n\r\n".format(host=host).encode()
        s.send(payload) # send a request to ask google for a main

        full_data = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            full_data += data
        print(full_data)
    

if __name__ == "__main__":
    client()