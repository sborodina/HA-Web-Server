import socket
import time
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 8080))
sock.listen(100)
sock.setblocking(0)

sockets = { sock.fileno(): sock }
kqueue = select.kqueue()
_sock_event = select.kevent(sock.fileno(),
    filter=select.KQ_FILTER_READ,
    flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE)
kqueue.control([_sock_event], 0, 0)

def request_handler(conn):
    data = conn.recv(1024)
    print("Client request: ", data)
    conn.send(b"Hellow world\n")
    sockets.pop(conn.fileno())
    conn.close()

def accept_handler(s):
    conn, address = s.accept()
    print("Client address: ", address[0], " Client port: ", address[1])
    conn.setblocking(0)
    sockets[conn.fileno()] = conn
    event = select.kevent(conn.fileno(),
        filter=select.KQ_FILTER_READ,
        flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE)
    kqueue.control([event], 0, 0)

while True:
    events = kqueue.control([], 100, None)
    for event in events:
        if event.ident == sock.fileno():
            accept_handler(sockets[event.ident])
        else:
            request_handler(sockets[event.ident])
