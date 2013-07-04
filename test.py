#! /usr/bin/env python

from time import sleep
from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import call
from sys import exit
from ConfigParser import SafeConfigParser

import smbus
import subprocess
import re
import socket
import fcntl
import struct
import paramiko
import socket
import signal

# DEFINE network interface
iface = 'wlan0'
 
# INI file config file
# Load in user name and IP address of command center 
# for the reverse shell test
parser = SafeConfigParser()
parser.read('./setting.conf')
 
ccIP = parser.get('reverse_shell', 'reverseDest')

lcd = Adafruit_CharLCDPlate(busnum = 1)

def TimeoutException(): 
	lcd.clear()
	lcd.backlight(lcd.OFF)
	exit()
 
def timeout(signum, frame):
    raise TimeoutException()
 
# Function which gets the IP address of a network interface
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
 
# Function which gets the Default Gateway IP address
def get_gateway(ifname):
 
    proc = subprocess.Popen("ip route list dev " + ifname + " | awk ' /^default/ {print $3}'", \
	shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 
    return_code = proc.wait()
    for line in proc.stdout:
        line
 
    return line

# ---------------------
# | Ping System Check |
# ---------------------
def do_ping_test():

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

# --------------------
# | Ping Default GW  |
# --------------------
def do_ping_default_gw():
	ip_gateway = get_gateway(iface)
 
	proc = subprocess.Popen ("ping -c 2 " + ip_gateway + " 2>&1", \
			shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
 
	return_code = proc.wait()
 
	# Read from pipes
	# stdout
	for line in proc.stdout:
	   if "loss" in line:
		   packet_loss = re.search('\d*%',line).group()
		   if int(packet_loss.split('%')[0]) > 0:
			   lcd.clear()
			   lcd.backlight(lcd.RED)
			   lcd.message("Ping Gateway:\nFailed")
			   sleep(1)
			   #print ip_gateway + packet_loss + " packet loss for gateway." 
		   else:
			   lcd.clear()
			   lcd.backlight(lcd.GREEN)
			   lcd.message("Ping Gateway:\nSuccess")
			   sleep(1)
			   #print "Gateway is reachable"  
	# stderr
	for line in proc.stderr:
		print("stderr: " + line.rstrip())

# --------------------
# | DHCP IP Address  |
# --------------------
def do_display_ip():
	try :
		ip_address = get_ip_address(iface)
		lcd.clear()
		lcd.backlight(lcd.GREEN)
		lcd.message("IP:\n" + ip_address)
		sleep(1)
	except :
		lcd.clear()
		lcd.backlight(lcd.RED)
		lcd.message("No IP obtained")
		sleep(1)

# -------------------
# |  Reverse Shell  |
# -------------------
def do_reverse_ssh():

	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ccIP, username='twi7ch', password='none')
	except paramiko.AuthenticationException:
		lcd.clear()
		lcd.backlight(lcd.GREEN)
		lcd.message("Reverse Tunnel:\nSuccess")
		sleep(1)
	except socket.error:
		lcd.clear()
		lcd.message("Reverse Shell: \nFailed")
		lcd.backlight(lcd.RED)
		sleep(1)



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
	sleep(5)


	# ---------------------
	# | Ping System Check |
	# ---------------------
	#do_ping_test();

	# --------------------
	# | Ping Default GW  |
	# --------------------
	#do_ping_default_gw();
 
	# --------------------
	# | DHCP IP Address  |
	# --------------------
 	do_display_ip();
	
	# -------------------
	# |  Reverse Shell  |
	# -------------------
	do_reverse_ssh()
 
	# Do we want to rerun the test?
	lcd.clear()
	lcd.backlight(lcd.YELLOW)
	lcd.message("Run test again?")
	sleep(1)
	lcd.clear()
 
	lcd.message("Yes = Left Btn\nNo = Right Btn")
	signal.signal(signal.SIGALRM, timeout)
 
	#change 5 to however many seconds you need
	signal.alarm(10)
	try:
		main()
	except TimeoutException:
		exit()
# Start the on board system check
init_test()			
 
main()