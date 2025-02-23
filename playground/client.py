import socket

def start_client(host="127.0.0.1", port=9999):
    # Local storage for records
    local_records = {}

    try:
        # Attempt to establish a connection to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"Connected to server at {host}:{port}")
    
    except ConnectionRefusedError:
        print("Connection refused by the server. Please ensure the server is running.")
        return  # Terminate the client execution
    
    except socket.error as e:
        print(f"Socket error: {e}")
        return  # Terminate the client execution
    
    try:
        # Synchronize with the server upon connection
        print("Synchronizing with the server...")
        client.send("sync".encode())
        response = client.recv(4096).decode()
        
        # Parse and store the synchronized records locally
        for line in response.split("\n"):
            if line:
                number, hash_val = line.split(":")
                local_records[int(number)] = hash_val
        
        print(f"Synchronized {len(local_records)} records from the server.")
        
        # Main loop for interacting with the server
        while True:
            command = input("Enter command (GET/EXIT): ").strip().upper()
            client.send(command.encode())
            
            if command == "EXIT":
                print("Exiting client...")
                break
            
            elif command == "GET":
                response = client.recv(4096).decode()
                print(f"Server Response:\n{response}")
                
                # Update local records with new data
                for line in response.split("\n"):
                    if line:
                        number, hash_val = line.split(":")
                        local_records[int(number)] = hash_val
                
                print(f"Updated local records. Total records: {len(local_records)}")
            
            else:
                print("Invalid command. Use 'GET' or 'EXIT'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    start_client()