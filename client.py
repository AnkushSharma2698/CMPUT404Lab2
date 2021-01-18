import socket
from pprint import pprint

def client():
    # utilizing context manager so no need to call s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("www.google.com", 80)) # Connect to google on port 80
        s.send(b"GET /\r\n") # send a request to ask google for a main
        data = s.recv(1024)
        pprint(data)
    

if __name__ == "__main__":
    client()