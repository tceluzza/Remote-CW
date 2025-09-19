import socket
import serial
import json
import logging

def keyDown(port):
  """CW key pressed"""
  port.dtr = True
  logging.info("Key pressed.")
  return 0  # 0 for success

def keyUp(port):
  """CW key released"""
  port.dtr = False
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
      return config['host'], config['port'], config['serial_port']
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
  
  

  host, port, serial_port = load_config()
  if not host or not port or not serial_port:
    return

  # Dictionary to map commands to functions
  commands = {
    "keydown": keyDown,
    "keyup": keyUp,
    "status": status
  }

  # Create a UDP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  # Open serial port for DTR CW sending
  logging.info(f"Initializing serial port {serial_port}")
  serial_ifce = serial.Serial(serial_port, 115200)
  serial_ifce.rts = serial_ifce.dtr = False 
  
  
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
        commands[command](serial_ifce)
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