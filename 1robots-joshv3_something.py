#!/usr/bin/env python
# -*- coding:utf-8 –*-
from serial.tools import list_ports
from pydobot import Dobot
from time import sleep
import datetime
import RPi.GPIO as GPIO
import os
import time
import random
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

inputSource = "console" # variable I'll use to check different input sources for debugging, testing and production; "console" and "buttons" only in use so far
simulate = False


digitInputLookup = {"1":"11",
					"2":"12",
					"3":"13",
					"4":"21",
					"5":"22",
					"6":"23",
					"7":"31",
					"8":"32",
					"9":"33"}
# file = open("position_log.txt","w")

class tokenPosition:
	# tokenPosition class - call this with (x, y, z, "blue") to define a token position with those input coordinates and current color of blue

	def __init__(self, xIn = 0, yIn = 0, zIn = 0, colorIn = "empty"):
		self.color = colorIn
		self.xPos = xIn
		self.yPos = yIn
		self.zPos = zIn

	# def updatePosition(self, )

# change these area/storage definitions to include the correct coordinates; can either change tokenPosition() to "tokenPosition(1, 2, 3, "blue")" or
# "tokenPosition(xIn = 1, yIn = 2, zIn = 3, color = "blue")"; using the latter, any can be omitted and the defaults will be used
playArea = {"11":tokenPosition(xIn = 10   , yIn = -48),
		    "12":tokenPosition(xIn = -18  , yIn = -28),
		    "13":tokenPosition(xIn = -47  , yIn = -9),
		    "21":tokenPosition(xIn = 29   , yIn = -19),
		    "22":tokenPosition(xIn = 0    , yIn = 0),
		    "23":tokenPosition(xIn = -28.5, yIn = 19.5),
		    "31":tokenPosition(xIn = 47.5 , yIn = 8),
		    "32":tokenPosition(xIn = 19.5 , yIn = 28),
		    "33":tokenPosition(xIn = -10  , yIn = 47)
}

orangeStorage = { "1":tokenPosition(xIn = 61.5, yIn = 168.5 , colorIn = "orange"),
			      "2":tokenPosition(xIn = 53.5, yIn = 136.5 , colorIn = "orange"),
			      "3":tokenPosition(xIn = 47  , yIn = 102   , colorIn = "orange"),
			      "4":tokenPosition(xIn = 93  , yIn = -163.5, colorIn = "orange"),
			      "5":tokenPosition(xIn = 88  , yIn = -128  , colorIn = "orange"),
			      "6":tokenPosition(xIn = 81.5, yIn = -94.5 , colorIn = "orange")
}

blueStorage = {   "1":tokenPosition(xIn = -113  , yIn = 5   , colorIn = "blue"),
			      "2":tokenPosition(xIn = -146.5, yIn = -1  , colorIn = "blue"),
			      "3":tokenPosition(xIn = -182  , yIn = -9  , colorIn = "blue"),
			      "4":tokenPosition(xIn = -120  , yIn = 38.5, colorIn = "blue"),
			      "5":tokenPosition(xIn = 47.5  , yIn = 8   , colorIn = "blue"),
			      "6":tokenPosition(xIn = -28.5 , yIn = 19.5, colorIn = "blue")
}

bootOffset = {"x":0,
				"y":0,
				"z":0}

# variables to hold the next tokens to grab; increment each time you grab one, or bad things will happen
nextBlue = 1
nextOrange = 1
tokensInPlay = 0

def printBoard(winningSet = []):
	if winningSet == []:
		print("Current board:\n")
		lineA = "{} | {} | {}".format(str(playArea["31"].color.upper()[0]), str(playArea["32"].color.upper()[0]), str(playArea["33"].color.upper()[0]) )
		lineB = "{} | {} | {}".format(str(playArea["21"].color.upper()[0]), str(playArea["22"].color.upper()[0]), str(playArea["23"].color.upper()[0]) )
		lineC = "{} | {} | {}\n".format(str(playArea["11"].color.upper()[0]), str(playArea["12"].color.upper()[0]), str(playArea["13"].color.upper()[0]) )
		print(lineA.replace("E", " "))
		print(lineB.replace("E", " "))
		print(lineC.replace("E", " "))
	else:
		print("Winning board:\n")
		lineA = "{} | {} | {}".format(str(playArea["31"].color.upper()[0]) if "31" in winningSet else str(playArea["31"].color[0]),
										str(playArea["32"].color.upper()[0]) if "32" in winningSet else str(playArea["32"].color[0]),
										str(playArea["33"].color.upper()[0]) if "33" in winningSet else str(playArea["33"].color[0]) )

		lineB = "{} | {} | {}".format(str(playArea["21"].color.upper()[0]) if "21" in winningSet else str(playArea["21"].color[0]),
										str(playArea["22"].color.upper()[0]) if "22" in winningSet else str(playArea["22"].color[0]),
										str(playArea["23"].color.upper()[0]) if "23" in winningSet else str(playArea["23"].color[0]) )

		lineC = "{} | {} | {}\n".format(str(playArea["11"].color.upper()[0]) if "11" in winningSet else str(playArea["11"].color[0]),
										str(playArea["12"].color.upper()[0]) if "12" in winningSet else str(playArea["12"].color[0]),
										str(playArea["13"].color.upper()[0]) if "13" in winningSet else str(playArea["13"].color[0]) )
		print(lineA.replace("e", " "))
		print(lineB.replace("e", " "))
		print(lineC.replace("e", " "))






def cleanup():
	global nextBlue
	global nextOrange
	global tokensInPlay
	global orangeStorage
	global blueStorage
	global playArea

	if simulate:
		# for resetPosition in playArea:
		# 	playArea[resetPosition].color = "empty"
		# for resetPosition in orangeStorage:
		# 	orangeStorage[resetPosition].color = "orange"
		# for resetPosition in blueStorage:
		# 	blueStorage[resetPosition].color = "blue"
		# nextOrange = 1
		# nextBlue = 1
		# tokensInPlay = 0

		for resetPosition in playArea:
			if playArea[resetPosition].color == "empty":
				pass
			elif playArea[resetPosition].color == "orange":
				moveToken(resetPosition, str(nextOrange-1), "orange", True)
				orangeStorage[str(nextOrange-1)].color = "orange"
				nextOrange -= 1
			elif playArea[resetPosition].color == "blue":
				moveToken(resetPosition, str(nextBlue-1), "blue", True)
				blueStorage[str(nextBlue-1)].color = "blue"
				nextBlue -= 1



	else:
		# do everything here we need to to reset the playing area
		# pass
		for resetPosition in playArea:
			if playArea[resetPosition].color == "empty":
				pass
			elif playArea[resetPosition].color == "orange":
				moveToken(resetPosition, str(nextOrange-1), "orange", True)
				orangeStorage[str(nextOrange-1)].color = "orange"
				nextOrange -= 1
			elif playArea[resetPosition].color == "blue":
				moveToken(resetPosition, str(nextBlue-1), "blue", True)
				blueStorage[str(nextBlue-1)].color = "blue"
				nextBlue -= 1



	print("RESET!")
	printBoard()




def moveToken(sourceSpace, targetSpace, colorToMove, clearing = False):
	print("moveToken called with: {} {} {}".format(str(sourceSpace), str(targetSpace), str(colorToMove)))
	global tokensInPlay
	global playArea

	# use sourcePosition and targetPosition to lookup the xyz values to call with
	if not clearing:
		targetPosition = playArea[str(targetSpace)]
		sourcePosition = orangeStorage[str(sourceSpace)] if colorToMove == "orange" else blueStorage[str(sourceSpace)]
		playArea[str(targetSpace)].color = colorToMove
		tokensInPlay += 1
	else:
		sourcePosition = playArea[str(sourceSpace)]
		targetPosition = orangeStorage[str(targetSpace)] if colorToMove == "orange" else blueStorage[str(targetSpace)]
		playArea[str(sourceSpace)].color = "empty"
		tokensInPlay -= 1

	if simulate:
		print("Would move token color {} from {} to {}.".format(colorToMove.upper(), "({}, {})".format(str(sourcePosition.xPos),str(sourcePosition.yPos)), "({}, {})".format(str(targetPosition.xPos),str(targetPosition.yPos))))

	else:
		port0 = list_ports.comports()[0].device
		device0 = Dobot(port=port0, verbose=False)
		(x, y, z, r, j1, j2, j3, j4) = device0.pose()
		#file.write(datetime.datetime.now())
		# posLog("Button1")
		# posLog(f'{x - x1} {y - y1} {z - z1} {j1} \n')

		# pick up next orange piece (need to figure out how to find next) (pick up first orange)
		device0.move_to(bootOffset["x"] + sourcePosition.xPos, bootOffset["y"] - sourcePosition.yPos, bootOffset["z"] + 20, 0, wait=True)
		device0.move_to(bootOffset["x"] + sourcePosition.xPos, bootOffset["y"] - sourcePosition.yPos, bootOffset["z"] - 1, 0, wait=False)
		device0.suck(True)
		device0.move_to(bootOffset["x"] + sourcePosition.xPos, bootOffset["y"] - sourcePosition.yPos, bootOffset["z"] + 20, 0, wait=False)

		# place piece in grid 1
		device0.move_to(bootOffset["x"] + targetPosition.xPos, bootOffset["y"] - targetPosition.yPos, bootOffset["z"] + 20, 0, wait=False)
		device0.move_to(bootOffset["x"] + targetPosition.xPos, bootOffset["y"] - targetPosition.yPos, bootOffset["z"] - 1, 0, wait=False)
		device0.suck(False)
		sleep(0.5)
		device0.move_to(bootOffset["x"] + targetPosition.xPos, bootOffset["y"] - targetPosition.yPos, bootOffset["z"] + 20, 0, wait=True)  # we wait until this movement is done before continuing

		# go to neutral pose
		device0.move_to(bootOffset["x"] - 36, bootOffset["y"] - 56, bootOffset["z"] + 20, 0, wait=True)





def playStep(orangeTarget):
	global nextOrange
	global nextBlue
	global orangeStorage
	global blueStorage
	if (playArea[orangeTarget].color == "empty"):

		if (nextOrange <= 6):
			moveToken(str(nextOrange), orangeTarget, "orange")
			orangeStorage[str(nextOrange)].color = "empty"
			nextOrange += 1
			print("Orange has moved.")
		else:
			print("No more orange pieces!?")
			return


		if (checkForWin("orange")):
			cleanup()
		else:
			if (nextBlue <= 6):
				moveToken(str(nextBlue), selectEmpty(), "blue")
				blueStorage[str(nextBlue)].color = "empty"
				nextBlue += 1
				print("Blue has moved.")
				printBoard()

			else:
				print("No more blue pieces!?")
				return
			if (checkForWin("blue")):
				cleanup()

	else:
		print("Select an empty space!")





def checkForWin(justPlayedColor):
	if tokensInPlay <= 4:
		print("Can't have won yet!")
		return False
	else:
		# do whatever we actually need to do to check for a win...
		# pass
		winningSet = []
		winningColor = ""

		if (playArea["11"].color == playArea["21"].color == playArea["31"].color):
			winningSet = ["11", "21", "31"]
			winningColor = playArea["11"].color

		if (playArea["11"].color == playArea["22"].color == playArea["33"].color):
			winningSet = ["11", "22", "33"]
			winningColor = playArea["11"].color

		if (playArea["11"].color == playArea["12"].color == playArea["13"].color):
			winningSet = ["11", "12", "13"]
			winningColor = playArea["11"].color

		if (playArea["12"].color == playArea["22"].color == playArea["32"].color):
			winningSet = ["12", "22", "32"]
			winningColor = playArea["12"].color

		if (playArea["13"].color == playArea["23"].color == playArea["33"].color):
			winningSet = ["13", "23", "33"]
			winningColor = playArea["13"].color

		if (playArea["13"].color == playArea["22"].color == playArea["31"].color):
			winningSet = ["13", "22", "31"]
			winningColor = playArea["13"].color

		if (playArea["21"].color == playArea["22"].color == playArea["23"].color):
			winningSet = ["21", "22", "23"]
			winningColor = playArea["21"].color

		if (playArea["31"].color == playArea["32"].color == playArea["33"].color):
			winningSet = ["31", "32", "33"]
			winningColor = playArea["31"].color

		if (winningColor != "" and winningColor != "empty"):
			print("{} WINS!\n".format(winningColor.upper()))
			printBoard(winningSet)
			return True
		elif tokensInPlay >= 9:
			print("Tie game!  NOBODY wins!")
			printBoard()
			return True
		else:
			return False





def selectEmpty():
	emptySpots = []
	for testSpot in playArea:
		if playArea[testSpot].color == "empty":
			# print("{} is empty.".format(testSpot))
			emptySpots.append(testSpot)
	if (emptySpots):
		# print(emptySpots)
		return random.choice(emptySpots)












# list of positions:
# grid1 = [9.905670166015625, -48.302337646484375, -1.3966445922851562, 46.005882263183594]
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
# print(f'{grid1}')



def posLog(textToLog = "posLog called without input?\n", targetFile = "position_log.txt"):
	with open(targetFile, "a+") as outputFile:
		outputFile.write(str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M'))+" "+str(textToLog))
	# break the file logging out into a custom function; this uses the preferred "with" method, which automatically closes the file after writing






def main():
	global bootOffset
	global nextBlue
	global nextOrange
	global tokensInPlay
	global orangeStorage
	global blueStorage
	global playArea

	if not simulate:
		port0 = list_ports.comports()[0].device
		device0 = Dobot(port=port0, verbose=True)
		(x1, y1, z1, r1, j1, j2, j3, j4) = device0.pose()
		bootOffset["x"] = x1
		bootOffset["y"] = y1
		bootOffset["z"] = z1

		# print(f'x:{x1} y:{y1} z:{z1} r:{0} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

		device0.speed(250, 250)
		device0.move_to(x1, y1, z1-1, 0, wait=False)
		device0.suck(True)
		device0.move_to(x1, y1, z1 + 20, 0, wait=False)  # we wait until this movement is done before continuing
		device0.move_to(x1 + 81.5, y1 - 94.5, z1 + 20, 0, wait=False)  # we wait until this movement is done before continuing
		device0.move_to(x1 + 81.5, y1 - 94.5, z1, 0, wait=False)  # we wait until this movement is done before continuing
		device0.suck(False)
		device0.move_to(x1 + 81.5, y1 - 94.5, z1 + 20, 0, wait=False)  # we wait until this movement is done before continuing
		device0.move_to(x1 - 36, y1 - 56, z1 + 20, 0, wait=False)



	try:
		os.remove("position_log.txt")
	except Exception as e:
		print("Exception while deleting file position_log.txt: "+str(e))





	# starting move to reposition home block from center of grid to last position of orange nest

	while(1):
		if (inputSource == "buttons"):
			if GPIO.input(button1)==0:
				playStep("11")

			if GPIO.input(button2)==0:
				playStep("12")

			if GPIO.input(button3)==0:
				playStep("13")

			if GPIO.input(button4)==0:
				playStep("21")

			if GPIO.input(button5)==0:
				playStep("22")

			if GPIO.input(button6)==0:
				playStep("23")

			if GPIO.input(button7)==0:
				playStep("31")

			if GPIO.input(button8)==0:
				playStep("32")

			if GPIO.input(button9)==0:
				playStep("33")

		elif (inputSource == "console"):
			while True:
				consoleInput = ""
				while consoleInput == "":
					consoleInput = ""
					consoleInput = input("Select a position to place your token.  Use the number pad orientation:\n")
					if len(consoleInput) == 1 and consoleInput.isdigit():
						playStep(digitInputLookup[str(consoleInput)])
					elif len(consoleInput) > 1:
						print("Please enter only one position!")
					elif not consoleInput.isdigit():
						print("Please enter only one digit!")




	# device.close()
	# # file.close()







if __name__ == '__main__':
	proc = main()
