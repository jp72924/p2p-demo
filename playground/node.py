import socket
import threading

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []  # List of connected peers
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def start_server(self):
        """Starts the server to listen for incoming connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Peer started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        """Accepts incoming connections from other peers."""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                self.peers.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

    def handle_client(self, client_socket):
        """Handles communication with a connected peer."""
        while self.running:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")
                else:
                    break
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()
        self.peers.remove(client_socket)

    def connect_to_peer(self, peer_host, peer_port):
        """Connects to another peer."""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            self.peers.append(peer_socket)
            print(f"Connected to peer at {peer_host}:{peer_port}")
            threading.Thread(target=self.handle_client, args=(peer_socket,), daemon=True).start()
        except Exception as e:
            print(f"Failed to connect to peer: {e}")

    def broadcast_message(self, message):
        """Broadcasts a message to all connected peers."""
        for peer in self.peers:
            try:
                peer.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send message to peer: {e}")

    def stop(self):
        """Stops the peer node."""
        self.running = False
        for peer in self.peers:
            peer.close()
        self.server_socket.close()
        print("Peer stopped.")

def main():
    host = '127.0.0.1'  # Localhost for testing
    port = int(input("Enter your peer's port: "))

    node = Node(host, port)
    node.start_server()

    while True:
        command = input("Enter command (connect/send/exit): ").strip().lower()
        if command == "connect":
            peer_host = input("Enter peer's host: ")
            peer_port = int(input("Enter peer's port: "))
            node.connect_to_peer(peer_host, peer_port)
        elif command == "send":
            message = input("Enter message to broadcast: ")
            node.broadcast_message(message)
        elif command == "exit":
            node.stop()
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()