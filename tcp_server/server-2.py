import asyncio
import logging

HOST = '0.0.0.0'
PORT = 6435

# Configure logging
logging.basicConfig(
  level=logging.DEBUG,  # Change to INFO or WARNING to reduce verbosity
  format='%(asctime)s %(levelname)s: %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("tcp_server")

active_client = None
client_lock = asyncio.Lock()

COMMANDS = {
  "HELLO": lambda: "Hello from server!",
  "STATUS": lambda: "Status: OK",
}

async def handle_client(reader, writer):
  global active_client

  addr = writer.get_extra_info('peername')
  client_addr = f"{addr[0]}:{addr[1]}"

  async with client_lock:
    if active_client is None:
      active_client = (reader, writer)
      logger.info(f"Client {client_addr} has control.")
    else:
      logger.warning(f"Rejected client {client_addr}: server busy.")
      writer.write(b"Server is busy. Try again later.\n")
      await writer.drain()
      writer.close()
      await writer.wait_closed()
      return

  try:
    while True:
      data = await reader.readline()
      if not data:
        logger.info(f"Client {client_addr} disconnected.")
        break

      command = data.decode().strip().upper()
      logger.debug(f"Received command from {client_addr}: {command}")

      func = COMMANDS.get(command)
      response = func() if func else "Unknown command."
      writer.write((response + '\n').encode())
      await writer.drain()

  except Exception as e:
    logger.error(f"Error with client {client_addr}: {e}")

  finally:
    async with client_lock:
      if active_client and active_client[1] is writer:
        active_client = None
        logger.info(f"Client {client_addr} released control.")
    writer.close()
    await writer.wait_closed()

async def main():
  server = await asyncio.start_server(handle_client, HOST, PORT)
  logger.info(f"Async server listening on {HOST}:{PORT}")
  async with server:
    await server.serve_forever()

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    logger.info("Server shutdown.")
