import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12347

clients = {}
messages = []

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        global clients, messages
        name = self.conn.recv(1024).decode("utf-8")
        clients[self.addr] = name

        # Notify all connected clients that a new user has joined
        join_message = f"{name} has joined the chat."
        for addr, client_name in clients.items():
            if addr != self.addr:
                clients[addr].sendall(join_message.encode("utf-8"))

        # Send the last 2 messages to the newly joined client
        for msg in messages[-2:]:
            self.conn.sendall(msg.encode("utf-8"))

        # Send the list of current users to the newly joined client
        users_list = "Current users: " + ", ".join(clients.values())
        self.conn.sendall(users_list.encode("utf-8"))

        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            messages.append(data.decode("utf-8"))
            for addr, client_name in clients.items():
                if addr != self.addr:
                    clients[addr].sendall(data)

        # Notify all connected clients that a user has left
        leave_message = f"{name} has left the chat."
        for addr, client_name in clients.items():
            if addr != self.addr:
                clients[addr].sendall(leave_message.encode("utf-8"))

        del clients[self.addr]
        self.conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    conn, addr = server.accept()
    client_thread = ClientThread(conn, addr)
    client_thread.start()
