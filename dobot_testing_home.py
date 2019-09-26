from serial.tools import list_ports

from pydobot import Dobot

port0 = list_ports.comports()[0].device
port1 = list_ports.comports()[1].device
device0 = Dobot(port=port0, verbose=True)


(x, y, z, r, j1, j2, j3, j4) = device0.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device1 = Dobot(port=port1, verbose=True)

(x, y, z, r, j1, j2, j3, j4) = device1.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device0.home(True)


device0.close()
device1.close()
