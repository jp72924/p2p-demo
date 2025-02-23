import socket
import time

def start_client(host='127.0.0.1', port=65432):
    """
    Start a client that sends 'ping' to the server and waits for 'pong'.
    """
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # for i in range(5):  # Send 5 ping messages
        while True:
            # Send 'ping' to the server
            client_socket.sendall("ping".encode())
            print(f"Sent: ping")

            # Wait for the server's response
            data = client_socket.recv(1024)
            print(f"Received: {data.decode().strip()}")

            time.sleep(1)  # Wait for 1 second before sending the next ping

if __name__ == "__main__":
    start_client()