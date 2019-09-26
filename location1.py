from serial.tools import list_ports

from pydobot import Dobot

port0 = list_ports.comports()[0].device
device = Dobot(port=port0, verbose=True)


(x, y, z, r, j1, j2, j3, j4) = device.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')


device.close()
