from pi_communicator import RaspberryPiServer  # Import the server class

def main():
    # Server configuration
    HOST = "0.0.0.0"  # Listen on all interfaces
    PORT = 5000       # Port to run the server

    # Initialize the server
    server = RaspberryPiServer(HOST, PORT, max_connections=1)  # Max connections set to 1 for single Pico
    print("Starting server...")

    try:
        # Start the server
        server.start_server()

        # Handle single Pico
        while True:
            if server.connections:
                client_address = list(server.connections.keys())[0]  # Get the first connected client
                print(f"Connected to Pico: {client_address}")

                # Example: Send a message to the Pico
                server.send_message(client_address, "Hello, Pico!")

                # Example: Receive and process messages from the Pico
                messages = server.get_received_messages(client_address)
                for message in messages:
                    print(f"Received from Pico: {message}")
            else:
                print("Waiting for Pico to connect...")

    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Ensure the server shuts down properly
        server.shutdown_server()

if __name__ == "__main__":
    main()
