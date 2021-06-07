import string
import socket
import sys
import os
import random
import time

IRC = None
ROUTES_LIST = []
FLAG = 0

def sendAllRoutes():
	
	global IRC
	
	print("Sending all routes.")
	IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel2", "UTF-8") + bytes(" :", "UTF-8") + bytes("Sending all routes.", "UTF-8") + bytes("\r\n", "UTF-8"))
	a_file = open("routes.txt", "r")
	lines = a_file.readlines()
	a_file.close()
	
	for line in lines:
		IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel2", "UTF-8") + bytes(" :", "UTF-8") + bytes("JOIN " + line, "UTF-8") + bytes("\r\n", "UTF-8"))
	IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel2", "UTF-8") + bytes(" :", "UTF-8") + bytes("All routes sent.", "UTF-8") + bytes("\r\n", "UTF-8"))
	print("All routes sent.")


def messageManagementIRC(text, flag):
	
	global IRC, ROUTES_LIST, FLAG
	
	if text.find("Sending all routes.") != -1:
		FLAG = 1
	
	if FLAG == 1:
		ROUTES_LIST.append(text)
	
	if text.find("All routes sent.") != -1:
		FLAG = 0
		print(ROUTES_LIST + "ROUTES LIST!!!!!!!!")
	
	print("Printing incoming msg = " + text)
	
	if text.find("PING") != -1:
		IRC.send(bytes("PONG ", "UTF-8") + bytes(text.split()[1], "UTF-8") + bytes("\r\n", "UTF-8"))
	elif text.find("JOIN") != -1 or text.find("QUIT") != -1:
		if text.find("End of /NAMES list") != -1:
			pass
		else:
			AddOrDeleteClient(text, flag)
	#else:
	#	sendPrivMessageIRC(text)

def sendPrivMessageIRC(msg):
	
	global IRC
	print("Printing PRIVMSG.")
	IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel2", "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))

def AddOrDeleteClient(msg, flag):
	
	#JOIN - QUIT = Palabras reservadas.
	# flag = 1 -> remote
	# flag = 0 -> local
	
	global IRC
	
	new_msg = msg.split(" ")
	#print(new_msg)
	
	if len(new_msg) == 2:
		if msg.find("JOIN") != -1:
			addHost(msg)
		elif msg.find("QUIT") != -1:
			deleteHost(msg)
	elif len(new_msg) > 2:
		if msg.find("JOIN") != -1:
			addHost(msg[3:])
		elif msg.find("QUIT") != -1:
			deleteHost(msg[3:])
		
	else:
		IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel2", "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))	
	
	#---------------------------------
	'''
	if msg.find("JOIN") != -1:
		if msg.find("PRIVMSG") != -1:
			addHost(msg.split(" ")[3:])
		else:			
			addHost(msg)
	if msg.find("QUIT") != -1:
		if msg.find("PRIVMSG") != -1:
			deleteHost(msg.split(" ")[3:])
		else:
			deleteHost(msg)
	
	IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel1", "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))
	'''

def addHost(raw_data):
	
	print("Adding host.")
	
	line = raw_data.split(" ")[1] + "\n"
	
	if line == "PRIVMSG\n":
		pass
	else:
		with open('routes.txt', 'a') as f:
			f.write(line)
				
	print("Host added.")
	sendAllRoutes()
	
def deleteHost(raw_data):
	
	print("Deleting host.")
	
	line = raw_data.split(" ")[1] + "\n"
	
	a_file = open("routes.txt", "r")
	lines = a_file.readlines()
	a_file.close()
	
	index = 0
	for i in range(len(lines)):
		if lines[i].find(line) != -1:
			index = i
	
	del lines[index]
	new_file = open("routes.txt", "w+")

	for line in lines:
		new_file.write(line)

	new_file.close()
	
	print("Host deleted.")
	#sendAllRoutes()
	
def closeServer():
	
	global IRC
	IRC.close()

def serverManagment(hostname):

	global IRC

	server = "209.97.147.243"
	channel = "#channel2"
	
	botnick = hostname[:10]
	IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	IRC.connect((server, 6667))
	time.sleep(2)
	IRC.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n", "UTF-8")) #user authentication
	time.sleep(2)
	IRC.send(bytes("NICK "+ botnick +"\n", "UTF-8"))
	time.sleep(2)
	IRC.send(bytes("JOIN "+ channel +"\n", "UTF-8"))
	time.sleep(2)
	
	flag = 0
	while(1):
		try:
			text = IRC.recv(2048).decode("UTF-8")
			if flag < 2:
				print(text + " Text from start.")
				flag += 1
			messageManagementIRC(text, 1)
				
		except Exception as IRCError:
			print('Error: {}'.format(IRCError))
	
