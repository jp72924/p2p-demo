import asyncio
import random
import websockets

async def handle_client(websocket):
    print("Client connected.")
    
    # Task to send random data to the client at unpredictable intervals
    async def send_random_data_to_client():
        try:
            while True:
                # Generate a random number and send it to the client
                data = random.randint(1, 100)
                print(f"Sending to client: {data}")
                await websocket.send(str(data))
                
                # Wait for a random interval between 1 and 5 seconds before sending again
                await asyncio.sleep(random.uniform(1, 5))
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")

    # Task to receive data from the client
    async def receive_data_from_client():
        try:
            async for message in websocket:
                print(f"Received from client: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")

    # Run both tasks concurrently
    await asyncio.gather(
        send_random_data_to_client(),
        receive_data_from_client()
    )

async def start_server():
    # Start the WebSocket server on localhost at port 8765
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(start_server())