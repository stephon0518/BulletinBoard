import socket
import threading

#HOST AND PORT SPECIFICALLY FOR THIS IMPLEMENTATION
HOST = "127.0.0.1"
PORT = 12340

#receiving messages from socket
def receive_messages(sockt):
    while True:
        data = sockt.recv(1024)
        if not data:
            break
        print(data.decode("utf-8"))

#connecting to server
def main():
    while True:
        #Command for input notifying the user the enter the connect command to connect to the server
        command = input("Enter connection command(with Host[space]port): ")

        
        if command.startswith("%connect"):
            try:
                _, host, port = command.split(" ")
                port = int(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, port))
                break
            except Exception as e:
                print("Unable to connect. Please check the host and port and try again.")

    #This is the name of the person trying to connect to the server and join either the public or private message board
    name = input("Enter your name: ")
    sock.sendall(name.encode("utf-8"))

    threading.Thread(target=receive_messages, args=(sock,)).start()

    #This is the start of all the Specified commands that the user would enter and what each will do on the client side 
    while True:
        command = input()
        #joining the public message board
        if command == "%join":
            sock.sendall(b"%join")
        #posting a message to the public message board
        elif command.startswith("%post"):
            try:
                _, subject, content = command.split(" ", 2)
                sock.sendall((f"%post {subject} {content}").encode("utf-8"))
            except ValueError:
                #prompting the user that if they enter the command wrong to put it in the right format
                print("Invalid post format.")
                print("Usage: %post <subject> <content>")

        #cheking for all the users in the public message board
        elif command == "%users":
            sock.sendall(b"%users")

        #This is to display a certain message that the user wants to see based on message ID, which is the order in which the messages were in
        elif command.startswith("%message"):
            try:
                _, message_id = command.split(" ")
                sock.sendall(("%message " + message_id).encode("utf-8"))
            except ValueError:
                #This is to prompt the user of an invalid message formatting
                print("Invalid message command format. Usage: %message <message_id>")

        #This command goes with the public message board, allowing the user to leave but reenter the server and function again
        elif command == "%leave":
            print("Leaving the public message board...")
            sock.sendall(b"%leave")
            sock.close()
            main()

        #THIS IS THE START OF THE PRIVATE MESSAGE BOARD PORTION OF THE PROJECT.

        #This first command will be for the choice of groups that you can join 
        elif command == "%groups":
            sock.sendall(b"%groups")

        #This groupjoin command allows the user to join whichever of the 5 groups that are available. They can join multiple
        elif command.startswith("%groupjoin"):
            sock.sendall(command.encode("utf-8"))

        #This allows the user to post in the specific group of their choosing. Group must me specified
        elif command.startswith("%grouppost"):
            sock.sendall(command.encode("utf-8"))

        #This Allows the user the see the other users that are in a specific group, to use this though, you must be in the group you are
        #trying to see the users for 
        elif command.startswith("%groupusers"):
            sock.sendall(command.encode("utf-8"))

        #This allows the user to leave whichever group they want, they can rejoin later
        elif command.startswith("%groupleave"):
            sock.sendall(command.encode("utf-8"))

        #The groupmessage command allows you to see a specific message based on message ID
        elif command.startswith("%groupmessage"):
            sock.sendall(command.encode("utf-8"))

        #The exit command basically makes it so that the user leaves the server completely and has to reconnect to enter. This is for both public and private message boards
        elif command == "%exit":
            print("Disconnecting from the server and exiting...")
            sock.sendall(b"%leave")
            sock.close()
            break

        else:
            #invalid command for the %join command
            print("Invalid command.")

if __name__ == "__main__":
    while True:
        main()
