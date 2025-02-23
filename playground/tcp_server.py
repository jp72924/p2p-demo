import socket

def start_server(host='127.0.0.1', port=65432):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((host, port))
        # Listen for incoming connections (queue up to 1 connection)
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        # Wait for a connection
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                # Receive data from the client
                data = conn.recv(1024)
                if not data:
                    # If no data is received, break the loop
                    print("Client disconnected.")
                    break
                print(f"Received: {data.decode()}")
                # Echo the received data back to the client
                conn.sendall(data)

if __name__ == "__main__":
    start_server()