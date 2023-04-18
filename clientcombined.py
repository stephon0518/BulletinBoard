import socket
import threading

HOST = "127.0.0.1"
PORT = 12340

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode("utf-8"))

def main():
    while True:
        command = input("Enter command: ")

        if command.startswith("%connect"):
            try:
                _, host, port = command.split(" ")
                port = int(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                break
            except Exception as e:
                print("Unable to connect. Please check the host and port and try again.")

    name = input("Enter your name: ")
    sock.sendall(name.encode("utf-8"))

    threading.Thread(target=receive_messages, args=(sock,)).start()

    while True:
        command = input()

        if command == "%join":
            sock.sendall(b"%join")

        elif command.startswith("%post"):
            try:
                _, subject, content = command.split(" ", 2)
                sock.sendall((f"%post {subject} {content}").encode("utf-8"))
            except ValueError:
                print("Invalid post format.")
                print("Usage: %post <subject> <content>")

        elif command == "%users":
            sock.sendall(b"%users")

        elif command.startswith("%message"):
            try:
                _, message_id = command.split(" ")
                sock.sendall(("%message " + message_id).encode("utf-8"))
            except ValueError:
                print("Invalid message command format. Usage: %message <message_id>")

        elif command == "%leave":
            print("Leaving the public message board...")
            sock.sendall(b"%leave")
            sock.close()
            main()

        elif command == "%groups":
            sock.sendall(b"%groups")

        elif command.startswith("%groupjoin"):
            sock.sendall(command.encode("utf-8"))

        elif command.startswith("%grouppost"):
            sock.sendall(command.encode("utf-8"))

        elif command.startswith("%groupusers"):
            sock.sendall(command.encode("utf-8"))

        elif command.startswith("%groupleave"):
            sock.sendall(command.encode("utf-8"))

        elif command.startswith("%groupmessage"):
            sock.sendall(command.encode("utf-8"))

        elif command == "%exit":
            print("Disconnecting from the server and exiting...")
            sock.close()
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
