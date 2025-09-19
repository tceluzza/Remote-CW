import tkinter as tk
from udp_server.udp_client import UdpClient

class App:
  def __init__(self, master):
    self.master = master
    self.master.title("UDP Command Sender")
    
    # Initialize the UdpClient
    self.client = UdpClient(config_file='udp_server/client_config.json')
    # if not self.client.sock:
    #   # If the client failed to initialize, disable the button
    #   print("Client failed to initialize. Please check client_config.json.")
    #   self.button = tk.Button(master, text="Connection Error", state=tk.DISABLED)
    # else:
    self.button = tk.Button(master, text="THIS IS A STRAIGHT KEY (I swear)", width=20, height=5)
      
    # Bind mouse events to the button
    self.button.bind("<Button-1>", self.keydown)
    self.button.bind("<ButtonRelease-1>", self.keyup)
    self.button.pack(padx=20, pady=20)
    
  def keydown(self, event):
    """Sends the 'keydown' command to the server."""
    print("Sending 'keydown' command...")
    response = self.client.send_command('keydown')
    print(f"Server response: {response}")

  def keyup(self, event):
    """Sends the 'keyup' command to the server."""
    print("Sending 'keyup' command...")
    response = self.client.send_command('keyup')
    print(f"Server response: {response}")

  def on_closing(self):
    """Closes the UDP client socket when the window is closed."""
    self.client.close()
    self.master.destroy()

if __name__ == "__main__":
  root = tk.Tk()
  app = App(root)
  root.protocol("WM_DELETE_WINDOW", app.on_closing)
  root.mainloop()
