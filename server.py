import socket
import threading

secret_key = ""

def read_word_from_file(file_path='serverKey.txt'):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    

def handle_client(client_socket, clients):
    try:
        while True:
            # Receive the word from the client
            word = client_socket.recv(1024).decode('utf-8')
            if word == "REQUEST_WORD":
                # Client requests a word, send a response
                response_word = read_word_from_file()
                client_socket.send(response_word.encode('utf-8'))
                print(f"Sent response word to client.")
            else:
                print(f"Received word from client.")
                with open('serverKey.txt', 'w') as file:
                    file.write(word)
                # Broadcast the word to other clients
                for other_client in clients:
                    if other_client != client_socket:
                        other_client.send(word.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Remove the client from the list when it disconnects
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {server_address}")

    clients = []

    try:
        while True:
            # Wait for a connection
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Add the client to the list
            clients.append(client_socket)

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, clients))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Close all client connections and the server socket
        for client_socket in clients:
            client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()
