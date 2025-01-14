import socket
import threading

class RaspberryPiServer:
    def __init__(self, host, port, max_connections=4):
        """
        Initialize the Raspberry Pi server.
        :param host: IP address to bind the server.
        :param port: Port to listen for connections.
        :param max_connections: Maximum number of simultaneous connections.
        """
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server_socket = None
        self.connections = {}
        self.received_messages = {}
        self.running = True

    def start_server(self):
        """
        Starts the server and listens for connections.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
            print(f"Server started on {self.host}:{self.port}")

            while self.running:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection accepted from {client_address}")

                # Store the client connection
                self.connections[client_address] = client_socket
                self.received_messages[client_address] = []

                # Start a thread for the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.shutdown_server()

    def handle_client(self, client_socket, client_address):
        """
        Handles communication with a connected client (Pico).
        """
        while self.running:
            try:
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"Message from {client_address}: {message}")
                    self.received_messages[client_address].append(message)
                    # Example: Echo the message back to the client
                    client_socket.sendall(f"Received: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Error with client {client_address}: {e}")
                break

        # Close the connection when done
        self.close_connection(client_address)

    def send_message(self, client_address, message):
        """
        Sends a message to a specific Pico.
        """
        if client_address in self.connections:
            try:
                self.connections[client_address].sendall(message.encode('utf-8'))
                print(f"Message sent to {client_address}: {message}")
            except Exception as e:
                print(f"Failed to send message to {client_address}: {e}")
        else:
            print(f"Client {client_address} not connected.")

    def broadcast_message(self, message):
        """
        Sends a message to all connected Picos.
        """
        for client_address in self.connections:
            self.send_message(client_address, message)

    def get_received_messages(self, client_address):
        """
        Retrieves and clears the list of received messages for a specific Pico.
        """
        if client_address in self.received_messages:
            messages = self.received_messages[client_address][:]
            self.received_messages[client_address].clear()
            return messages
        return []

    def close_connection(self, client_address):
        """
        Closes the connection with a specific Pico.
        """
        if client_address in self.connections:
            try:
                self.connections[client_address].close()
                print(f"Connection with {client_address} closed.")
            except Exception as e:
                print(f"Error closing connection with {client_address}: {e}")
            finally:
                del self.connections[client_address]
                del self.received_messages[client_address]

    def shutdown_server(self):
        """
        Shuts down the server and closes all connections.
        """
        self.running = False
        for client_address in list(self.connections.keys()):
            self.close_connection(client_address)
        if self.server_socket:
            self.server_socket.close()
        print("Server shut down.")