#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 8003

def proxy_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the proxy server
        s.connect((HOST, PORT))
        # Send the Request to the proxy
        host = 'www.google.com'
        payload = "GET / HTTP/1.0\r\nHost: {host}\r\n\r\n".format(host=host).encode()
        s.sendall(payload)

        # Loop to recieve the entire message from proxy server
        msg = b""
        while True:
            response = s.recv(4096)
            if not response:
                break
            msg += response
        print(msg)

if __name__ == "__main__":
    proxy_client()