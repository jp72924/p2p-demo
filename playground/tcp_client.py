import socket

def start_client(host='127.0.0.1', port=65432):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send data to the server
        message = "Hello, Server!"
        client_socket.sendall(message.encode())
        print(f"Sent: {message}")

        # Receive data from the server
        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")

if __name__ == "__main__":
    start_client()