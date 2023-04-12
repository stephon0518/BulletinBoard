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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    name = input("Enter your name: ")
    sock.sendall(name.encode("utf-8"))

    threading.Thread(target=receive_messages, args=(sock,)).start()

    while True:
        command = input()

        if command == "%groups":
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

        elif command == "%quit":
            print("Disconnecting from the server and exiting...")
            sock.close()
            break

        else:
            print("Invalid command.")

    sock.close()

if __name__ == "__main__":
    main()
