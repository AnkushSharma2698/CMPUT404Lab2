import socket
import sys
from multiprocessing import Process


HOST, PORT = 'localhost', 8001

def echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            p = Process(target=echo_handler, args=(conn, addr))
            p.daemon = True
            p.start()
            print("Starting subprocess", p)

def echo_handler(conn, addr):
    print("Connector: ", addr)
    data = conn.recv(4096)
    conn.sendall(data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    echo_server()