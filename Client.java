import java.io.*;
import java.net.*;

public class Client {
    private static final String SERVER_ADDRESS = "localhost";
    private static final int SERVER_PORT = 12345;

    public static void main(String[] args) {
        try (Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT)) {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));

            // Create a separate thread for receiving messages from the server
            Thread receiveMessages = new Thread(() -> {
                try {
                    while (true) {
                        String serverMessage = in.readLine();
                        if (serverMessage == null) {
                            break;
                        }
                        System.out.println(serverMessage);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            receiveMessages.start();

            // Main loop for sending messages to the server
            while (true) {
                String input = userInput.readLine();
                if (input == null || input.equalsIgnoreCase("quit")) {
                    break;
                }

                // Send the input to the server.
                out.println(input);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Implement additional methods for handling user input and server responses.
}
