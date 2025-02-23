import asyncio
import random
import websockets

async def communicate_with_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        
        # Task to send random data to the server at unpredictable intervals
        async def send_random_data_to_server():
            try:
                while True:
                    # Generate a random number and send it to the server
                    data = random.randint(1, 100)
                    print(f"Sending to server: {data}")
                    await websocket.send(str(data))
                    
                    # Wait for a random interval between 1 and 5 seconds before sending again
                    await asyncio.sleep(random.uniform(1, 5))
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")

        # Task to receive data from the server
        async def receive_data_from_server():
            try:
                async for message in websocket:
                    print(f"Received from server: {message}")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")

        # Run both tasks concurrently
        await asyncio.gather(
            send_random_data_to_server(),
            receive_data_from_server()
        )

if __name__ == "__main__":
    asyncio.run(communicate_with_server())