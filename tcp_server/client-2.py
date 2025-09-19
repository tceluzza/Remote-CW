import asyncio
import sys
import aioconsole

HOST = '127.0.0.1'
PORT = 6435

async def read_from_server(reader, stop_event):
  try:
    while not stop_event.is_set():
      data = await reader.readline()
      if not data:
        print("[!] Server closed the connection.")
        stop_event.set()
        break
      print(f"Server response: {data.decode().strip()}")
  except Exception as e:
    print(f"[!] Error reading from server: {e}")
    stop_event.set()

async def write_to_server(writer, stop_event):
  try:
    while not stop_event.is_set():
      cmd = await aioconsole.ainput()
      if stop_event.is_set():
        break
      if cmd.strip().upper() == "EXIT":
        print("[*] Closing connection...")
        stop_event.set()
        break
      writer.write((cmd + '\n').encode())
      await writer.drain()
  except Exception as e:
    print(f"[!] Error sending to server: {e}")
    stop_event.set()
        
async def main():
  stop_event = asyncio.Event()
  try:
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"[+] Connected to server at {HOST}:{PORT}")

    tasks = [
      asyncio.create_task(read_from_server(reader, stop_event)),
      asyncio.create_task(write_to_server(writer, stop_event)),
    ]

    await stop_event.wait()

    for task in tasks:
      task.cancel()
      try:
        await task
      except asyncio.CancelledError:
        pass

    writer.close()
    await writer.wait_closed()

  except ConnectionRefusedError:
    print("[!] Cannot connect to server.")
  except Exception as e:
    print(f"[!] Client error: {e}")

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("\n[*] Client shut down.")
