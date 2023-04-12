import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12340

connections = {}
client_names = {}
messages = []
message_counter = 0

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        global connections, client_names, messages, message_counter
        name = self.conn.recv(1024).decode("utf-8")
        joined = False

        while True:
            data = self.conn.recv(1024)
            if not data:
                break

            command = data.decode("utf-8").split(" ", 1)[0]

            if command == "%join":
                if not joined:
                    connections[self.addr] = self.conn
                    client_names[self.addr] = name
                    joined = True
                    self.conn.sendall("You have joined the message board.".encode("utf-8"))

                    for msg in messages[-2:]:
                        self.conn.sendall(msg.encode("utf-8"))

                else:
                    self.conn.sendall("You have already joined the message board.".encode("utf-8"))

            elif command == "%post":
                subject, content = data.decode("utf-8").split(" ", 1)[1].split(" ", 1)
                message_counter += 1
                post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_message = f"Message ID {message_counter}, {name}, {post_date}, {subject}: {content}\n"
                messages.append(formatted_message)

                for addr, conn in connections.items():
                    if addr != self.addr:
                        conn.sendall(("%post " + formatted_message).encode())

            elif command == "%users":
                users_list = "Current users: " + ", ".join(client_names.values())
                self.conn.sendall(users_list.encode("utf-8"))

            elif command == "%message":
                message_id = int(data.decode("utf-8").split(" ", 1)[1])
                if 0 < message_id <= len(messages):
                    self.conn.sendall(messages[message_id - 1].encode("utf-8"))
                else:
                    self.conn.sendall("Invalid message ID.".encode("utf-8"))

            elif command == "%leave":
                if joined:
                    del connections[self.addr]
                    del client_names[self.addr]
                    for addr, conn in connections.items():
                        conn.sendall((f"{name} has left the group.").encode())
                    break
                else:
                    self.conn.sendall("You are not in the group.".encode("utf-8"))

        self.conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    conn, addr = server.accept()
    client_thread = ClientThread(conn, addr)
    client_thread.start()
