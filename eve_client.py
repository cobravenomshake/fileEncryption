import socket
from ping3 import ping, verbose_ping

def read_word_from_file(file_path='sharedKey.txt'):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None


def scan_ports(host, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust timeout as needed
        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"Port {port} is open")
            open_ports.append(port)

        sock.close()

    return open_ports

# Example usage:
host_to_scan = 'localhost'
start_port = 12340
end_port = 12350
open_ports = scan_ports(host_to_scan, start_port, end_port)
print("Open ports:", open_ports)

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', open_ports[0])
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
                print(f"Received word from server.")
                with open('bobKey.txt', 'w') as file:
                    file.write("ndfvkjsdfvbladkf vlajkhfvblakdf vklasbvdlk")
            else:
                print("Invalid input. Please enter S or R.")

    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_client()