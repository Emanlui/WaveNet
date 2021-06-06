import string
import socket
import sys
import os
import random
import time

IRC = None

def sendMessageIRC(msg):
	
	global IRC
	#print("Printing msg.")

	if msg.find("JOIN") != -1:
		addHost(msg)
	if msg.find("QUIT") != -1:
		deleteHost(msg)
	else:
		IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes("#channel1", "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))

def getHostData(raw_string):
	
	raw_string = raw_string[1:]
	raw_string = raw_string.split("!")
	
	hostname = raw_string[0]
	raw_string = raw_string[1].split("@")
	
	iden = raw_string[0]
	raw_string = raw_string[1].split(" ")
	
	ip = raw_string[0]
	line = ""
	line += ip
	line += "|"
	line += hostname
	line += "|"
	line += "6667"
	line += "\n"    
	line = line.replace("\n", "")
	line += "\n"
	
	return line

def addHost(raw_data):
	
	print("Adding host.")
	print(raw_data)
	#line = getHostData(raw_data)
	line = raw_data.split(" ")[1] + "\n"
	
	if line == "JOIN\n":
		line = getHostData(raw_data)
	with open('routes.txt', 'a') as f:
		f.write(line)
	
	print("Host added.")
	
def deleteHost(raw_data):
	
	print("Deleting host.")
	print(raw_data)
	line = raw_data.split(" ")[1] + "\n"
	if line == "QUIT\n":
		line = getHostData(raw_data)
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
	
def closeServer():
	
	global IRC

	IRC.close()

def serverManagment(hostname):

	global IRC

	server = "209.97.147.243"       #settings
	channel = "#channel1"
	
	#getVals = list([val for val in hostname if val.isalnum()])
	#hostname_tmp = "".join(getVals)
	#hostname="tmp_hostname"
	
	botnick = hostname[:10]
	IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
	IRC.connect((server, 6667))                                                      #connects to the server
	time.sleep(3)
	IRC.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n", "UTF-8")) #user authentication
	time.sleep(3)
	IRC.send(bytes("NICK "+ botnick +"\n", "UTF-8"))                            #sets nick
	time.sleep(3)
	IRC.send(bytes("JOIN "+ channel +"\n", "UTF-8"))        #join the chan
	#print("Enviando mensaje\n")
	time.sleep(3)
	#irc.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))
	#irc.close()
	
	while(1):
		try:
			text = IRC.recv(2048).decode("UTF-8")   #receive the text
			print (text)
			if text.find("PING") != -1:
				IRC.send(bytes("PONG ", "UTF-8") + bytes(text.split()[1], "UTF-8") + bytes("\r\n", "UTF-8"))
			if text.find("PRIVMSG") != -1: #Verifica si alguien manda un msg.
				print("")
				#IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(text, "UTF-8") + bytes("\r\n", "UTF-8"))
			if text.find("JOIN") != -1: #Verifica si entra alguien.
				#irc.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(text, "UTF-8") + bytes("\r\n", "UTF-8"))
				if text.find("End of /NAMES list") != -1:
					continue;
				else:
					addHost(text)
			if text.find("QUIT") != -1: #Verifica si sale alguien.
				#irc.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(text, "UTF-8") + bytes("\r\n", "UTF-8"))
				deleteHost(text)
				
		except Exception:
			pass
	
#serverManagment()
