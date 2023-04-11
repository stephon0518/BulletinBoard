import socket
import threading

HOST = "127.0.0.1"
PORT = 12347

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode("utf-8"))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

name = input("Enter your name: ")
sock.sendall(name.encode("utf-8"))

threading.Thread(target=receive_messages, args=(sock,)).start()

while True:
    msg = input("Enter your message: ")
    if msg.lower() == "quit":
        break
    sock.sendall(msg.encode("utf-8"))

sock.close()
