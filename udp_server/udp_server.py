import socket
import json
import logging

def keyDown():
  """Executes 'function_a'."""
  logging.info("Key pressed.")
  return 0  # 0 for success

def keyUp():
  """Executes 'function_b'."""
  logging.info("Key released.")
  return 0  # 0 for success

def status():
  """Returns server status"""
  return 0  # if we got here, the server must be working

def load_config():
  """Loads host and port from server_config.json."""
  try:
    with open('server_config.json', 'r') as f:
      config = json.load(f)
      return config['host'], config['port']
  except (FileNotFoundError, KeyError) as e:
    logging.error(f"Error loading server config: {e}")
    return None, None

def run_server():
  """Runs the UDP server."""
  # Configure logging
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )
  
  host, port = load_config()
  if not host or not port:
    return

  # Dictionary to map commands to functions
  commands = {
    "keydown": keyDown,
    "keyup": keyUp,
    "status": status
  }

  # Create a UDP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  # Bind the socket to the host and port
  server_address = (host, port)
  logging.info(f"Starting UDP server on {host}:{port}")
  sock.bind(server_address)

  try:
    while True:
      logging.debug("Waiting for a command...")
      data, address = sock.recvfrom(4096)
      command = data.decode().strip().lower()
      logging.debug(f"Received command '{command}' from {address}")

      if command in commands:
        commands[command]()
        response = b'0'  # Success
      else:
        response = b'1'  # Failure
        logging.warning(f"Unknown command received: {command}")

      # Send the response back to the client
      sock.sendto(response, address)
      logging.debug("Response sent.")
  except KeyboardInterrupt:
    logging.info("Server is shutting down.")
  finally:
    sock.close()

if __name__ == "__main__":
  run_server()