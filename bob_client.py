# client.py
import socket

word = ""
def read_word_from_file(file_path='serverKey.txt'):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)
    print(f"Connected to {server_address}")

    try:
        while True:
            # Read the word from the file or user input
            reply = str(input("Do you want to send or receive a word? Reply S/R: "))
            
            if reply == "S":
                word = read_word_from_file()
                # Send the word to the server
                client_socket.send(word.encode('utf-8'))
                print(f"Sent word to server!")
            elif reply == "R":
                # Request a word from the server
                client_socket.send("REQUEST_WORD".encode('utf-8'))
                received_word = client_socket.recv(1024).decode('utf-8')
                print(received_word)
                print(f"Received word from server.")
                with open('bobKey.txt', 'w') as file:
                    file.write(received_word)
            else:
                print("Invalid input. Please enter S or R.")

    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_client()
