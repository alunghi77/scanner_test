#! /usr/bin/env python

from time import sleep
from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

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


# Start the on board system check
init_test()			
 
main()