from serial.tools import list_ports

from pydobot import Dobot

port0 = list_ports.comports()[0].device
device = Dobot(port=port0, verbose=True)


(x, y, z, r, j1, j2, j3, j4) = device.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

#device.speed(100, 100)
#device.move_to(x + 20, y+20, z+20, r-20, wait=False)
#device.suck(True)
#device.move_to(x, y, z, r, wait=False)  # we wait until this movement is done before continuing
#device.suck(False)

device.close()
