import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12340

connections = {}
groups = {
    'Group1': {'users': {}, 'messages': []},
    'Group2': {'users': {}, 'messages': []},
    'Group3': {'users': {}, 'messages': []},
    'Group4': {'users': {}, 'messages': []},
    'Group5': {'users': {}, 'messages': []},
}

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        global groups
        name = self.conn.recv(1024).decode("utf-8")
        user_groups = set()

        self.conn.sendall(("Available groups: " + ', '.join(groups.keys())).encode("utf-8"))

        while True:
            data = self.conn.recv(1024)
            if not data:
                break

            command_parts = data.decode("utf-8").split(" ", 1)
            command = command_parts[0]

            if command == "%groupjoin":
                group_name = command_parts[1]
                if group_name in groups:
                    groups[group_name]['users'][self.addr] = name
                    user_groups.add(group_name)
                    self.conn.sendall(f"You have joined {group_name}.".encode("utf-8"))

                    # Notify other users in the group that a new user has joined
                    for other_addr in groups[group_name]['users']:
                        if other_addr != self.addr:
                            connections[other_addr].sendall(f"{name} has joined {group_name}.".encode("utf-8"))
                            
                else:
                    self.conn.sendall("Invalid group name.".encode("utf-8"))

            elif command == "%grouppost":
                group_name, subject, content = command_parts[1].split(" ", 2)
                if group_name in user_groups:
                    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"{name}, {post_date}, {subject}: {content}"
                    groups[group_name]['messages'].append(formatted_message)

                    for addr in groups[group_name]['users']:
                        if addr != self.addr:
                            connections[addr].sendall(("%grouppost " + formatted_message).encode())
                else:
                    self.conn.sendall("You are not a member of this group.".encode("utf-8"))

            elif command == "%groupusers":
                group_name = command_parts[1]
                if group_name in user_groups:
                    users_list = "Users in {}: ".format(group_name) + ", ".join(groups[group_name]['users'].values())
                    self.conn.sendall(users_list.encode("utf-8"))
                else:
                    self.conn.sendall("You are not a member of this group.".encode("utf-8"))

            elif command == "%groupleave":
                group_name = command_parts[1]
                if group_name in user_groups:
                    del groups[group_name]['users'][self.addr]
                    user_groups.remove(group_name)
                    self.conn.sendall(f"You have left {group_name}.".encode("utf-8"))

                    # Notify other users in the group
                    leave_message = f"{name} has left {group_name}."
                    for addr in groups[group_name]['users']:
                        connections[addr].sendall(leave_message.encode("utf-8"))

                else:
                    self.conn.sendall("You are not a member of this group.".encode("utf-8"))

            elif command == "%groupmessage":
                group_name, message_id = command_parts[1].split(" ", 1)
                message_id = int(message_id)
                if group_name in user_groups:
                    if 0 < message_id <= len(groups[group_name]['messages']):
                        self.conn.sendall(groups[group_name]['messages'][message_id - 1].encode("utf-8"))
                    else:
                        self.conn.sendall("Invalid message ID.".encode("utf-8"))
                else:
                    self.conn.sendall("You are not a member of this group.".encode("utf-8"))

        for group_name in user_groups:
            del groups[group_name]['users'][self.addr]

        self.conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    conn, addr = server.accept()
    connections[addr] = conn
    client_thread = ClientThread(conn, addr)
    client_thread.start()

