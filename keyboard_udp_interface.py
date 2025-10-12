import keyboard
from udp_server.udp_client import UdpClient

class KeyListener:
    def __init__(self):
        self.client = UdpClient(config_file='udp_server/client_config.json')
        print("Listening for ',' and '.' key events. Press ESC to exit.")

        # Register key events
        keyboard.on_press_key(43, self.leftdown)
        keyboard.on_release_key(43, self.leftup)
        keyboard.on_press_key(47, self.rightdown)
        keyboard.on_release_key(47, self.rightup)

        # Wait until ESC is pressed
        keyboard.wait('esc')
        self.client.close()
        print("Exiting.")

    def leftdown(self, event):
        print("Sending 'leftdown' command...")
        response = self.client.send_command('keydown')
        print(f"Server response: {response}")

    def leftup(self, event):
        print("Sending 'leftup' command...")
        response = self.client.send_command('keyup')
        print(f"Server response: {response}")

    def rightdown(self, event):
        print("Sending 'rightdown' command...")
        response = self.client.send_command('keydown')
        print(f"Server response: {response}")

    def rightup(self, event):
        print("Sending 'rightup' command...")
        response = self.client.send_command('keyup')
        print(f"Server response: {response}")

if __name__ == "__main__":
    KeyListener()