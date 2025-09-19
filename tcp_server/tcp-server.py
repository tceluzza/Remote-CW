import socket
import time

HOST = '0.0.0.0'
PORT = 6435
client_connected = False

def say_hello():
  return "Hello from server!"

def get_status():
  return "Status: OK"

COMMANDS = {
  'HELLO': say_hello,
  'STATUS': get_status,
}

def handle_client(conn, addr):
  global client_connected
  print(f"[+] Connected to {addr}")
  with conn:
    conn.settimeout(60)
    while True:
      try:
        data = conn.recv(1024)
        if not data:
          print("[-] Client disconnected.")
          break

        command = data.decode('utf-8').strip().upper()
        print(f"[{addr}] Received: {command}")

        func = COMMANDS.get(command)
        response = func() if func else "Unknown command."
        conn.sendall((response + '\n').encode('utf-8'))

      except socket.timeout:
        print("[!] Connection timed out.")
        break
      except Exception as e:
        print(f"[!] Error: {e}")
        break

  client_connected = False
  print("[*] Ready for new connection.")

def start_server():
  global client_connected

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    s.settimeout(1.0)  # Periodically check for new connections

    print(f"[+] Server listening on {HOST}:{PORT}")

    while True:
      try:
        if client_connected:
          time.sleep(0.5)  # Don’t accept new clients while one is connected
          continue

        try:
          conn, addr = s.accept()
        except socket.timeout:
          continue  # Check again in the next loop cycle

        client_connected = True
        handle_client(conn, addr)

      except KeyboardInterrupt:
        print("\n[!] Server interrupted by user.")
        break
      except Exception as e:
        print(f"[!] Server error: {e}")
        break

  print("[*] Server shutting down.")

if __name__ == "__main__":
  start_server()
