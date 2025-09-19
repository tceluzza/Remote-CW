import serial
import tkinter as tk

speed = 0.1
port = serial.Serial('COM4', 115200)
# port.open()

port.rts=port.dtr=False

class App:
    def __init__(self, master):
        self.master=master
        self.sending = False
        self.button = tk.Button(master, text="SK",)
                               # command=self.startsend)
        self.button.pack()
        self.button.bind("<Button-1>", self.startsend)
        self.button.bind("<ButtonRelease-1>", self.stopsend)

    def startsend(self, event):
        print("start")
        self.sending = True
        port.dtr = True
        print (port.dtr)
    def stopsend(self, event):
        print("stop")
        self.sending = False
        port.dtr=False
        print (port.dtr)
root = tk.Tk()
app =App(root)
root.mainloop()
