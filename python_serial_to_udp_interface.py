import serial
from udp_server.udp_client import UdpClient


TONE_FREQ = 600  # Hz
SAMPLE_RATE = 44100

# --- Main Program ---
def main():
    # Initialize UDP client
    client = UdpClient(config_file='udp_server/client_config.json')

    # Open serial connection
    ser = serial.Serial('/dev/cu.usbmodem21101', 9600, timeout=1)
    print("Connected to Arduino")


    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        print(f"Received: {line}")

        if line == "KEY_DOWN":
            response = client.send_command("KEY_DOWN")
            print(f"Sent UDP: KEY_DOWN | Response: {response}")
        elif line == "KEY_UP":
            response = client.send_command("KEY_UP")
            print(f"Sent UDP: KEY_UP | Response: {response}")

if __name__ == "__main__":
    main()