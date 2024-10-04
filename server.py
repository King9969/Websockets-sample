import asyncio
import websockets

# A set to store all connected clients
connected_clients = set()

async def handler(websocket, path):
    # Register client
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Received from {websocket.remote_address}: {message}")
            # Broadcast the message to all connected clients except the sender
            await broadcast(f"Client {websocket.remote_address}: {message}", websocket)
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def broadcast(message, sender):
    # Send the message to all clients except the sender
    if connected_clients:
        # Create tasks for each send operation
        tasks = [
            asyncio.create_task(client.send(message))
            for client in connected_clients
            if client != sender
        ]
        if tasks:
            # Await the completion of all tasks
            await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server is running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
