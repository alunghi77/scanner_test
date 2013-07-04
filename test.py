#! /usr/bin/env python

from time import sleep
from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import call

import smbus
import subprocess
import re
import socket
import fcntl
import struct
import paramiko
import socket
import signal

lcd = Adafruit_CharLCDPlate(busnum = 1)

def main():
	while 1:
 
		if (lcd.buttonPressed(lcd.LEFT)):
			signal.alarm(0)
			init_test()
 
		if (lcd.buttonPressed(lcd.RIGHT)):
			# End of system check
			lcd.backlight(lcd.OFF)
			exit()


# Function for running all of the system tests
def init_test():
 
	# clear display
	lcd.clear()
 
    # Commented out to speed up overal test time
	# Starting On Board System Check
	lcd.backlight(lcd.BLUE)
	lcd.message("Welcome to \nGD Scanner Unit ")
	sleep(21)

	# ---------------------
	# | Ping System Check |
	# ---------------------
 
	# Put stderr and stdout into pipes
	proc = subprocess.Popen("ping -c 2 google.com 2>&1", \
			shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 
	return_code = proc.wait()
 
	# Read from pipes
	# stdout
	for line in proc.stdout:
		if "loss" in line:
			packet_loss = progress = re.search('\d*%',line).group()
			if int(packet_loss.split('%')[0]) > 0:
				lcd.clear()
				lcd.backlight(lcd.RED)
				lcd.message("Ping Google:\nFailed")
				sleep(1)
				#print packet_loss + " packet loss."
			else:
				lcd.clear()
				lcd.backlight(lcd.GREEN)
				lcd.message("Ping Google:\nSuccess")
				sleep(1)
	#stderr
	for line in proc.stderr:
		print("stderr: " + line.rstrip())


# Start the on board system check
init_test()			
 
main()