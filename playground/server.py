import socket
import threading
import hashlib
import random
import time

# Shared data structure to store the latest records
latest_records = []  # List to store the last N records
MAX_RECORDS = 10  # Maximum number of records to keep in memory
lock = threading.Lock()  # Lock to ensure thread-safe access to shared data

def generate_random_numbers():
    """Generator to continuously yield random numbers."""
    while True:
        yield random.randint(0, 10**6)  # Adjust range as needed

def hash_number(number):
    """Hashes a number using SHA-256 and returns the hexadecimal digest."""
    return hashlib.sha256(str(number).encode()).hexdigest()

def record_generator():
    """
    Continuously generates random numbers, hashes them, and updates the latest records.
    Runs in a separate thread.
    """
    global latest_records
    generator = generate_random_numbers()
    while True:
        number = next(generator)
        hashed_value = hash_number(number)
        
        # Update the shared records safely
        with lock:
            latest_records.append({"number": number, "hash": hashed_value})
            if len(latest_records) > MAX_RECORDS:
                latest_records.pop(0)  # Keep only the last MAX_RECORDS
        
        print(f"Generated Record: Number = {number}, Hash = {hashed_value}")
        time.sleep(2.5)  # Simulate some delay between generations

def handle_client(client_socket, client_id):
    """
    Handles communication with a single client.
    Sends the latest records to the client upon request.
    """
    print(f"Client {client_id} connected.")
    try:
        while True:
            # Wait for the client to send a request
            request = client_socket.recv(1024).decode().strip().lower()
            
            if request == "get":
                # Retrieve the latest records safely
                with lock:
                    response = "\n".join(
                        [f"Number: {r['number']}, Hash: {r['hash']}" for r in latest_records]
                    )
                
                # Send the records to the client
                client_socket.send(response.encode())
            
            elif request == "sync":
                # Send all records for synchronization
                with lock:
                    response = "\n".join(
                        [f"{r['number']}:{r['hash']}" for r in latest_records]
                    )
                
                client_socket.send(response.encode())
            
            elif request == "exit":
                print(f"Client {client_id} disconnected.")
                break
            
            else:
                client_socket.send("Invalid command. Use 'GET', 'SYNC', or 'EXIT'.".encode())
    
    except Exception as e:
        print(f"Error handling client {client_id}: {e}")
    
    finally:
        client_socket.close()

def start_server(host="127.0.0.1", port=9999):
    """
    Starts the TCP server and listens for up to two clients.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)  # Allow up to 2 clients
    print(f"Server started on {host}:{port}")

    # Start the record generation thread
    threading.Thread(target=record_generator, daemon=True).start()

    client_id = 1
    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")
        
        # Limit the number of concurrent clients to 2
        if threading.active_count() > 3:  # Main thread + 2 client threads
            client_socket.send("Server is busy. Please try again later.".encode())
            client_socket.close()
            continue
        
        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket, client_id), daemon=True).start()
        client_id += 1

if __name__ == "__main__":
    start_server()