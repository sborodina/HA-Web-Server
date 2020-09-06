import socket
import time
import threading
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 8080))
sock.listen(100)

def handler(conn):
    time.sleep(10)
    conn.send(b"Hellow world\n")
    conn.close()

while True:
    conn, address = sock.accept()
    print("Client address: ", address[0], " Client port: ", address[1])
    data = conn.recv(1024)
    print("Client request: ", data)
    thread = threading.Thread(target=handler, args=(conn, ))
    thread.start()
