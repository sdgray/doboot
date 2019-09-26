
from serial.tools import list_ports
from pydobot import Dobot
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
button1=11
button2=13
button3=15
button4=29
button5=31
button6=33
button7=35
button8=37
button9=12
button10=16
button11=18
button12=22
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button8,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button9,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button10,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button11,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button12,GPIO.IN,pull_up_down=GPIO.PUD_UP)

file = open("position_log.txt","w")

port0 = list_ports.comports()[0].device
device0 = Dobot(port=port0, verbose=True)
(x, y, z, r, j1, j2, j3, j4) = device0.pose()

print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')



while(1):
        if GPIO.input(button1)==0:
            print("Button1")
            sleep(0.1)
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
            file.write(f'{x} {y} {z} {j1} '"\n")
        if GPIO.input(button2)==0:
            print("Button2")
            sleep(0.1)
            device0.speed(100, 100)
            device0.move_to(x + 20, y+20, z+20, r-20, wait=False)
            device0.suck(True)
            device0.move_to(x, y, z, r, wait=False)  # we wait until this movement is done before continuing
            device0.suck(False)
        if GPIO.input(button3)==0:
            print("Button3")
            sleep(0.1)
        if GPIO.input(button4)==0:
            print("Button4")
            sleep(0.1)
        if GPIO.input(button5)==0:
            print("Button5")
            sleep(0.1)
        if GPIO.input(button6)==0:
            print("Button6")
            sleep(0.1)
        if GPIO.input(button7)==0:
            print("Button7")
            sleep(0.1)
        if GPIO.input(button8)==0:
            print("Button8")
            sleep(0.1)
        if GPIO.input(button9)==0:
            print("Button9")
            sleep(0.1)
        if GPIO.input(button10)==0:
            print("Button10")
            sleep(0.1)
        if GPIO.input(button11)==0:
            print("Button11")
            sleep(0.1)
        if GPIO.input(button12)==0:
            print("Button12")
            sleep(0.1)
            




device.close()
file.close()
