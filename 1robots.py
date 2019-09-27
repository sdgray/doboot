
from serial.tools import list_ports
from pydobot import Dobot
from time import sleep
import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
button3=11
button9=13
button6=15
button4=29
button7=31
button1=33
button10=35
button11=37
button12=12
button2=16
button8=18
button5=22
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
(x1, y1, z1, r1, j1, j2, j3, j4) = device0.pose()

print(f'x:{x1} y:{y1} z:{z1} r:{r1} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

# list of positions:
grid1 = [9.905670166015625, -48.302337646484375, -1.3966445922851562, 46.005882263183594]
#-18.1324462890625 -28.022430419921875 -0.7948226928710938 55.349998474121094 
#-47.30333709716797 -8.884170532226562 -0.41034698486328125 64.77352905273438 
#29.216445922851562 -19.2491455078125 -0.39328765869140625 47.46176528930664 
#0.09710693359375 -0.2574920654296875 -0.09612274169921875 55.53529357910156 
#-28.509811401367188 19.504852294921875 -1.3744583129882812 63.63529586791992 
#-28.445518493652344 19.63458251953125 -1.338134765625 63.63529586791992 
#47.712738037109375 8.380828857421875 0.33329010009765625 48.494117736816406 
#19.4027099609375 27.86944580078125 0.9934959411621094 55.53529357910156 
#-9.961669921875 47.03465270996094 -0.6227149963378906 62.735294342041016 
#-112.80430793762207 4.7194061279296875 -2.107147216796875 83.01176452636719 
#-146.5410032272339 -0.7677154541015625 -0.7043685913085938 92.40882110595703 
#-182.06145477294922 -9.070053100585938 -1.4661026000976562 102.86470794677734 
#-119.75960159301758 38.44541931152344 -1.177001953125 85.63235473632812 
#-153.58052444458008 32.4923095703125 -1.5585479736328125 93.78529357910156 
#-187.68125915527344 25.672927856445312 -0.6574020385742188 102.30882263183594 
#61.46484375 -168.75434112548828 -1.5637741088867188 9.344118118286133 
#53.721527099609375 -136.31397247314453 -1.3992233276367188 18.794116973876953 
#47.233062744140625 -102.14649963378906 -1.31304931640625 28.217647552490234 
#93.19606018066406 -163.42331314086914 -1.0623626708984375 9.370588302612305 
#87.77362060546875 -128.08709716796875 -1.6643829345703125 18.026470184326172 
#81.58253479003906 -94.47595977783203 -0.2721710205078125 25.994117736816406 
print(f'{grid1}')

# starting move to reposition home block from center of grid to last position of orange nest
device0.speed(250, 250)
device0.move_to(x1, y1, z1-1, r1, wait=False)
device0.suck(True)
device0.move_to(x1, y1, z1 + 20, r1, wait=False)  # we wait until this movement is done before continuing
device0.move_to(x1 + 81.5, y1 - 94.5, z1 + 20, r1, wait=False)  # we wait until this movement is done before continuing
device0.move_to(x1 + 81.5, y1 - 94.5, z1, r1, wait=False)  # we wait until this movement is done before continuing
device0.suck(False)
device0.move_to(x1 + 81.5, y1 - 94.5, z1 + 20, r1, wait=False)  # we wait until this movement is done before continuing
device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


while(1):
        if GPIO.input(button1)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button1")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up first orange)
            device0.move_to(x1 + 61.5, y1 - 168.5, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 61.5, y1 - 168.5, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 + 61.5, y1 - 168.5, z1 + 20, r1, wait=False)

            # place piece in grid 1
            device0.move_to(x1 + 10, y1 - 48, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 10, y1 - 48, z1 - 1, r1, wait=False)
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 + 10, y1 - 48, z1 + 20, r1, wait=False)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button2)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button2")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up second orange)
            device0.move_to(x1 + 53.5, y1 - 136.5, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 53.5, y1 - 136.5, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 + 53.5, y1 - 136.5, z1 + 20, r1, wait=False)

            # place piece in grid 2
            device0.move_to(x1 - 18, y1 - 28, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 18, y1 - 28, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 - 18, y1 - 28, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button3)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button3")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up third orange)
            device0.move_to(x1 + 47, y1 - 102, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 47, y1 - 102, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 + 47, y1 - 102, z1 + 20, r1, wait=False)

            # place piece in grid 3
            device0.move_to(x1 - 47, y1 - 9, z1 + 20, r1, wait=False) 
            device0.move_to(x1 - 47, y1 - 9, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 - 47, y1 - 9, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button4)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button4")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up fourth orange)
            device0.move_to(x1 + 93, y1 - 163.5, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 93, y1 - 163.5, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 + 93, y1 - 163.5, z1 + 20, r1, wait=False)

            # place piece in grid 4
            device0.move_to(x1 + 29, y1 - 19, z1 + 20, r1, wait=False) 
            device0.move_to(x1 + 29, y1 - 19, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 + 29, y1 - 19, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button5)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button5")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up fifth orange)
            device0.move_to(x1 + 88, y1 - 128, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 88, y1 - 128, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 + 88, y1 - 128, z1 + 20, r1, wait=False)

            # place piece in grid 5
            device0.move_to(x1 + 0, y1 - 0, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 0, y1 - 0, z1 - 1, r1, wait=False)
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 + 0, y1 - 0, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button6)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button6")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up sixth orange)
            device0.move_to(x1 + 81.5, y1 - 94.5, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 81.5, y1 - 94.5, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 + 81.5, y1 - 94.5, z1 + 20, r1, wait=False)

            # place piece in grid 6
            device0.move_to(x1 - 28.5, y1 + 19.5, z1 + 20, r1, wait=False) 
            device0.move_to(x1 - 28.5, y1 + 19.5, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 - 28.5, y1 + 19.5, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button7)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button7")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up first blue)
            device0.move_to(x1 - 113, y1 + 5, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 113, y1 + 5, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 - 113, y1 + 5, z1 + 20, r1, wait=False)

            # place piece in grid 7
            device0.move_to(x1 + 47.5, y1 + 8, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 47.5, y1 + 8, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 + 47.5, y1 + 8, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button8)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button8")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up second blue)
            device0.move_to(x1 - 146.5, y1 - 1, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 146.5, y1 - 1, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 - 146.5, y1 - 1, z1 + 20, r1, wait=False)

            # place piece in grid 8
            device0.move_to(x1 + 19.5, y1 + 28, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 19.5, y1 + 28, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 + 19.5, y1 + 28, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button9)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button9")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up third blue)
            device0.move_to(x1 - 182, y1 - 9, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 182, y1 - 9, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 - 182, y1 - 9, z1 + 20, r1, wait=False)

            # place piece in grid 9
            device0.move_to(x1 - 10, y1 + 47, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 10, y1 + 47, z1 - 1, r1, wait=False) 
            device0.suck(False)
            sleep(0.5)
            device0.move_to(x1 - 10, y1 + 47, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            # go to neutral pose
            device0.move_to(x1 - 36, y1 - 56, z1 + 20, r1, wait=False)


        if GPIO.input(button10)==0:
            device0 = Dobot(port=port0, verbose=True)
            (x, y, z, r, j1, j2, j3, j4) = device0.pose()
            #file.write(datetime.datetime.now())
            file.write("Button10 - This is not a real button!")
            file.write(f'{x - x1} {y - y1} {z - z1} {j1} '"\n")

            # pick up next orange piece (need to figure out how to find next) (pick up fourth blue)
            device0.move_to(x1 - 120, y1 + 38.5, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 120, y1 + 38.5, z1 - 1, r1, wait=False)
            device0.suck(True)
            device0.move_to(x1 - 120, y1 + 38.5, z1 + 20, r1, wait=False)

            # place piece in grid 8
            device0.move_to(x1 + 19.5, y1 - 28, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 19.5, y1 - 28, z1 - 1, r1, wait=False)
            device0.suck(False)
            device0.move_to(x1 + 19.5, y1 - 28, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing


        if GPIO.input(button11)==0:
            
            # place piece in grid 7
            device0.move_to(x1 + 47.5, y1 + 8, z1 + 20, r1, wait=False)
            device0.move_to(x1 + 47.5, y1 + 8, z1 - 1, r1, wait=False) 
            device0.suck(False)
            device0.move_to(x1 + 47.5, y1 + 8, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

        if GPIO.input(button12)==0:

            # place piece in grid 6
            device0.move_to(x1 - 28.5, y1 + 19.5, z1 + 20, r1, wait=False)
            device0.move_to(x1 - 28.5, y1 + 19.5, z1 - 1, r1, wait=False) 
            device0.suck(False)
            device0.move_to(x1 - 28.5, y1 + 19.5, 48, z1 + 20, r1, wait=True)  # we wait until this movement is done before continuing

            




device.close()
file.close()
