import asyncio
import websockets

async def send_messages(websocket):
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, input)
        if message.lower() == 'exit':
            print("Closing connection")
            await websocket.close()
            break
        await websocket.send(message)

async def receive_messages(websocket):
    try:
        async for message in websocket:
            print(f"\n{message}")
    except websockets.ConnectionClosed:
        pass

async def communicate():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the server")
            # Run send and receive tasks concurrently
            send_task = asyncio.create_task(send_messages(websocket))
            receive_task = asyncio.create_task(receive_messages(websocket))
            done, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
    except ConnectionRefusedError:
        print("Failed to connect to the server")

if __name__ == "__main__":
    asyncio.run(communicate())
