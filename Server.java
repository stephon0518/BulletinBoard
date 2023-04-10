import java.io.*;
import java.net.*;
import java.util.*;

public class Server {
    private static final int PORT = 12345;
    private static List<ClientHandler> clients = Collections.synchronizedList(new ArrayList<>());

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server is running...");

            while (true) {
                Socket socket = serverSocket.accept();
                ClientHandler clientHandler = new ClientHandler(socket);
                clients.add(clientHandler);
                new Thread(clientHandler).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Implement additional methods for handling messages, clients, and groups.
    public static void broadcast(String message) {
        for (ClientHandler client : clients) {
            client.sendMessage(message);
        }
    }

    public static void removeClient(ClientHandler client) {
        clients.remove(client);
    }

    public static String getClientsList() {
        StringBuilder clientsList = new StringBuilder("Connected clients: ");
        for (ClientHandler client : clients) {
            clientsList.append(client.getUsername()).append(", ");
        }
        return clientsList.toString();
    }

    private String username;

    public String getUsername() {
        return username;
    }

    public void sendMessage(String message) {
        out.println(message);
    }

    @Override
    public void run() {
    try {
        in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        out = new PrintWriter(socket.getOutputStream(), true);

        // User authentication (setting a username)
        while (true) {
            out.println("Enter your username: ");
            username = in.readLine();
            if (username == null || username.trim().isEmpty()) {
                out.println("Invalid username, try again.");
            } else {
                break;
            }
        }

        // Broadcast the user's joining to all clients
        Server.broadcast(username + " has joined the chat.");
        out.println("Welcome, " + username + "!");

        // Main loop for receiving and broadcasting messages
        while (true) {
            String message = in.readLine();
            if (message == null || message.equalsIgnoreCase("quit")) {
                break;
            }
            Server.broadcast(username + ": " + message);
        }
    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        Server.removeClient(this);
        Server.broadcast(username + " has left the chat.");
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


    
}
