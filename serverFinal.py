import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12340
#initializing
connections = {}
client_names = {}
messages = []
message_count = 0
#format for list of 5 groups
groups = {
    'Group1': {'users': {}, 'messages': []},
    'Group2': {'users': {}, 'messages': []},
    'Group3': {'users': {}, 'messages': []},
    'Group4': {'users': {}, 'messages': []},
    'Group5': {'users': {}, 'messages': []},
}

#clients connecting to server
class ClientThread(threading.Thread):
    def __init__(self, connect, addr):
        threading.Thread.__init__(self)
        self.connect = connect
        self.addr = addr

    def run(self):
        global connections, client_names, messages, message_count, groups
        name = self.connect.recv(1024).decode("utf-8")
        joined = False
        user_groups = set()

        while True:
            data = self.connect.recv(1024)
            if not data:
                break

            command_pieces = data.decode("utf-8").split(" ", 1)
            command = command_pieces[0]
            #joining public message board
            if command == "%join":
                if not joined:
                    connections[self.addr] = self.connect
                    client_names[self.addr] = name
                    joined = True
                    self.connect.sendall("You have joined the message board.".encode("utf-8"))

                    # Notify other users that a new user has joined
                    join_message = f"{name} has joined the message board."
                    for addr, conn in connections.items():
                        if addr != self.addr:
                            conn.sendall(join_message.encode("utf-8"))

                    users_list = "Users who joined earlier including you: " + ", ".join(client_names.values())
                    self.connect.sendall(users_list.encode("utf-8"))

                    for msg in messages[-2:]:
                        self.connect.sendall(msg.encode("utf-8"))

                else:
                    self.connect.sendall("You have already joined the message board.".encode("utf-8"))
            #posting to public message board
            elif command == "%post":
                if len(command_pieces) > 1:
                    try:
                        subject, content = command_pieces[1].split(" ", 1)
                    except ValueError:
                        self.connect.sendall("Invalid post format. Usage: %post <subject> <content>".encode("utf-8"))
                        continue

                    message_count += 1
                    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"\nMessage ID {message_count}, {name}, {post_date}, {subject}: {content}\n"
                    messages.append(formatted_message)

                    for addr, conn in connections.items():
                        if addr != self.addr:
                            conn.sendall(("%post " + formatted_message).encode())
                else:
                    self.connect.sendall("Invalid post format. Usage: %post <subject> <content>".encode("utf-8"))

            #obtaing list of users in public message board
            elif command == "%users":
                users_list = "Current users: " + ", ".join(client_names.values())
                self.connect.sendall(users_list.encode("utf-8"))

            #obtaining specific message in public message board
            elif command == "%message":
                message_id = int(command_pieces[1])
                if 0 < message_id <= len(messages):
                    self.connect.sendall(messages[message_id - 1].encode("utf-8"))
                else:
                    self.connect.sendall("Invalid message ID.".encode("utf-8"))
            #outputting list of private groups to join
            elif command == "%groups":
                groups_list = "Available groups: " + ", ".join(groups.keys())
                self.connect.sendall(groups_list.encode("utf-8"))

            #joining private groups
            elif command == "%groupjoin":
                group_name = command_pieces[1]
                if group_name in groups:
                    groups[group_name]['users'][self.addr] = name
                    user_groups.add(group_name)
                    self.connect.sendall(f"You have joined {group_name}.".encode("utf-8"))

                    users_list = "Users who joined earlier: " + ", ".join(groups[group_name]['users'].values()) + "\n"

                    self.connect.sendall(users_list.encode("utf-8"))

                    # Send the last 2 messages in the group
                    for message in groups[group_name]['messages'][-2:]:
                        self.connect.sendall(message.encode("utf-8"))

                    # Notify other users in the group that a new user has joined
                    for other_addr in groups[group_name]['users']:
                        if other_addr != self.addr:
                            connections[other_addr].sendall(f"{name} has joined {group_name}.".encode("utf-8"))

                else:
                    self.connect.sendall("Invalid group name.".encode("utf-8"))
            #posting to private group
            elif command == "%grouppost":
                group_name, subject, content = command_pieces[1].split(" ", 2)
                if group_name in user_groups:
                    post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"{name}, {post_date}, {subject}: {content}\n"
                    groups[group_name]['messages'].append(formatted_message)

                    for addr in groups[group_name]['users']:
                        if addr != self.addr:
                            connections[addr].sendall(("%grouppost " + formatted_message).encode())
                else:
                    self.connect.sendall("You are not a member of this group.".encode("utf-8"))

            #obtaining list of users in private group
            elif command == "%groupusers":
                group_name = command_pieces[1]
                if group_name in user_groups:
                    # Directly use the users in the group
                    users_list = "Users in {}: ".format(group_name) + ", ".join(groups[group_name]['users'].values())
                    self.connect.sendall(users_list.encode("utf-8"))
                else:
                    self.connect.sendall("You are not a member of this group.".encode("utf-8"))

            #leaving private groups
            elif command == "%groupleave":
                group_name = command_pieces[1]
                if group_name in user_groups:
                    del groups[group_name]['users'][self.addr]
                    user_groups.remove(group_name)
                    self.connect.sendall(f"You have left {group_name}.".encode("utf-8"))

                    # Notify other users in the group
                    leave_message = f"{name} has left {group_name}."
                    for addr in groups[group_name]['users']:
                        connections[addr].sendall(leave_message.encode("utf-8"))

                else:
                    self.connect.sendall("You are not a member of this group.".encode("utf-8"))
            #obtaining specific private group message
            elif command == "%groupmessage":
                group_name, message_id = command_pieces[1].split(" ", 1)
                message_id = int(message_id)
                if group_name in user_groups:
                    if 0 < message_id <= len(groups[group_name]['messages']):
                        self.connect.sendall(groups[group_name]['messages'][message_id - 1].encode("utf-8"))
                    else:
                        self.connect.sendall("Invalid message ID.".encode("utf-8"))
                else:
                    self.connect.sendall("You are not a member of this group.".encode("utf-8"))

            #leaving private group
            elif command == "%leave":
                if joined:
                    del connections[self.addr]
                    del client_names[self.addr]

                    # Notify other users that the user has left
                    leave_message = f"{name} has left the message board."
                    for addr, conn in connections.items():
                        conn.sendall((f"{name} has left the public message board.").encode())
                    break
                else:
                    self.connect.sendall("You are not in the group.".encode("utf-8"))

        for group_name in user_groups:
            del groups[group_name]['users'][self.addr]

        self.connect.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    conn, addr = server.accept()
    connections[addr] = conn
    client_thread = ClientThread(conn, addr)
    client_thread.start()
