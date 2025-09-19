import serial
import time

speed = 0.1
port = serial.Serial('COM4', 115200)
# port.open()

port.rts=port.dtr=False

r = port.rts
d = port.dtr
print(f'RTS: {r}\tDTR: {d}')

port.dtr = True

r = port.rts
d = port.dtr
print(f'RTS: {r}\tDTR: {d}')

time.sleep(1) #SECONDS NOT MS

port.dtr = False

r = port.rts
d = port.dtr
print(f'RTS: {r}\tDTR: {d}')

def dit():
    port.dtr = True
    time.sleep(speed)
    port.dtr = False
def dah():
    port.dtr = True
    time.sleep(speed * 3)
    port.dtr = False
def symbgap():
    time.sleep(speed)
def chargap():
    time.sleep(speed * 3)
def wordgap():
    time.sleep(speed * 7)

stringCW = '...- ...- ...-/-.. ./-. .---- - .--- -.-.'

for i in range(len(stringCW)):
    if i != 0:
        if stringCW[i] in ['.', '-'] and stringCW[i-1] in ['.', '-']:
            symbgap()
    match stringCW[i]:
        case '.':
            dit()
        case '-':
            dah()
        case ' ':
            chargap()
        case '/':
            wordgap()
        