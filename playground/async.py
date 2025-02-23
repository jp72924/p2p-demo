import asyncio
import random
import socket

# Constants for connection
HOST = '127.0.0.1'  # Localhost IP address
PORT = 65432        # Port to listen on/connect to

# Function to handle sending messages at random intervals
async def send_messages(writer):
    try:
        while True:
            # Generate a random message and interval
            message = f"Message from sender: {random.randint(1, 100)}"
            interval = random.uniform(1, 5)  # Random delay between 1 and 5 seconds
            
            print(f"Sending: {message}")
            writer.write(message.encode())
            await writer.drain()  # Ensure data is sent
            
            # Wait for a random interval before sending the next message
            await asyncio.sleep(interval)
    except ConnectionResetError:
        print("Connection was closed by the receiver.")
    finally:
        writer.close()
        await writer.wait_closed()

# Function to handle receiving messages
async def receive_messages(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("No more data received. Closing connection.")
                break
            
            print(f"Received: {data.decode()}")
    except ConnectionResetError:
        print("Connection was closed by the sender.")
    finally:
        print("Closing receiver.")

# Main function to set up client or server mode
async def main(is_server=True):
    if is_server:
        # Server mode: Listen for incoming connections
        server = await asyncio.start_server(
            handle_client, HOST, PORT)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
    else:
        # Client mode: Connect to the server
        reader, writer = await asyncio.open_connection(HOST, PORT)
        
        # Start sending and receiving tasks concurrently
        await asyncio.gather(
            send_messages(writer),
            receive_messages(reader)
        )

# Handle incoming client connections (server-side)
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    # Start sending and receiving tasks concurrently
    await asyncio.gather(
        send_messages(writer),
        receive_messages(reader)
    )

if __name__ == "__main__":
    # Run as a server or client based on user choice
    import sys
    is_server = '--server' in sys.argv
    
    asyncio.run(main(is_server))