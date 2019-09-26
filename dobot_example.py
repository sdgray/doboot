from serial.tools import list_ports

from pydobot import Dobot

port0 = list_ports.comports()[0].device
#port1 = list_ports.comports()[1].device
device0 = Dobot(port=port0, verbose=True)


(x, y, z, r, j1, j2, j3, j4) = device0.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

##device1 = Dobot(port=port1, verbose=True)

##(x, y, z, r, j1, j2, j3, j4) = device1.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

print({device0.pose()})

device0.speed(100, 100)
device0.move_to(244, -0, -49.12, -0.93, wait=True) 
device0.suck(True)
device0.move_to(244, -0, -39.12, -0.93, wait=True) 
device0.suck(False)

##device0.speed(100, 100)
#device1.speed(100, 100)
##device0.move_to(x + 20, y+20, z+20, r-20, wait=False)
#device1.move_to(x + 20, y+20, z-20, r+20, wait=False)
##device0.suck(True)
##device0.move_to(x, y, z, r, wait=False)
#device1.move_to(x, y, z, r, wait=True)  # we wait until this movement is done before continuing
##device0.suck(False)

device0.close()
#device1.close()
