import socket
import threading
import time

def handle_client(conn, addr):
    """
    Handle communication with a single client.
    """
    print(f"Connected by {addr}")
    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected.")
                break
            
            message = data.decode()
            print(f"Received from {addr}: {message}")
            
            if message.strip().lower() == "ping":
                # Send 'pong' back to the client
                conn.sendall("pong\n".encode())
            else:
                # If the message is not 'ping', echo it back
                conn.sendall(data)

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_server(host='127.0.0.1', port=65432):
    """
    Start the server and listen for incoming connections.
    """
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((host, port))
        # Listen for incoming connections (queue up to 2 connections)
        server_socket.listen(2)
        print(f"Server listening on {host}:{port}")

        while True:
            # Wait for a connection
            conn, addr = server_socket.accept()

            # Limit the number of concurrent clients to 2
            if threading.active_count() > 3:  # Main thread + 2 client threads
                conn.send("Server is busy. Please try again later.".encode())
                conn.close()
                continue

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()