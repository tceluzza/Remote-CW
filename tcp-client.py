import socket

HOST = '127.0.0.1'
PORT = 6435

def main():
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      print(f"[+] Connected to server at {HOST}:{PORT}")

      while True:
        cmd = input("Enter command (HELLO, STATUS, EXIT): ").strip()
        if not cmd:
          continue

        if cmd.upper() == 'EXIT':
          print("[*] Closing connection...")
          break

        s.sendall((cmd + '\n').encode('utf-8'))
        response = s.recv(1024).decode('utf-8').strip()
        print(f"Server response: {response}")

  except ConnectionRefusedError:
    print("[!] Cannot connect to the server. Is it running?")
  except Exception as e:
    print(f"[!] Client error: {e}")

if __name__ == "__main__":
  main()
