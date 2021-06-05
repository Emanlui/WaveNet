import string
import socket
import sys
import os
import random
import time

def sendMessageIRC(msg):
	irc.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))

	

def getHostData(raw_string):
	
	raw_string = raw_string[1:]
	raw_string = raw_string.split("!")
	
	hostname = raw_string[0]
	raw_string = raw_string[1].split("@")
	iden = raw_string[0]
	raw_string = raw_string[1].split(" ")
	ip = raw_string[0]
	key = sendKeys(ip, 6667)
	key = key.decode("utf-8")
	
	key = key[31:]
	key = key[:-30]
	
	line = ""
	line += ip
	line += "|"
	line += hostname
	line += "|"
	line += "6667"
	line += "|"
	line += key
	line += "\n"	
	line = line.replace("\n", "")
	line += "\n"
	
	return line

def addHost(raw_data):
	line = getHostData(raw_data)
	with open('host.routes', 'a') as f:
		f.write(line)
	
	print("Host added.")
	
def deleteHost(raw_data):
	
	line = getHostData(raw_data)
	
	a_file = open("host.routes", "r")

	lines = a_file.readlines()
	a_file.close()
	#print(lines)
	index = lines.index(line)

	del lines[index]

	new_file = open("host.routes", "w+")

	for line in lines:
		new_file.write(line)

	new_file.close()
	
	print("Host deleted.")
	
def closeServer(irc):
	
	irc.close()
	
	print("Server closed succesfully.")
	
	return 0

def serverStartUp():

	print("Starting server up.")
	
	server = "209.97.147.243" #settings
	channel = "#channel1"
	hostname = "bot_name"
	
	botnick = hostname[:10]
	IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
	IRC.connect((server, 6667))                                                      #connects to the server
	time.sleep(2)
	IRC.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n", "UTF-8")) #user authentication
	time.sleep(2)
	IRC.send(bytes("NICK "+ botnick +"\n", "UTF-8"))                            #sets nick
	time.sleep(2)
	IRC.send(bytes("JOIN "+ channel +"\n", "UTF-8"))        #join the chan
	
	print("Server stareted up succesfully.")
	
	while(1):
		try:
			text = IRC.recv(2048).decode("UTF-8")   #receive the text
			print (text)
			if text.find("PING") != -1:
				IRC.send(bytes("PONG ", "UTF-8") + bytes(text.split()[1], "UTF-8") + bytes("\r\n", "UTF-8"))
			if text.find("PRIVMSG") != -1: #Verifica si alguien manda un msg.
				IRC.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(text, "UTF-8") + bytes("\r\n", "UTF-8"))
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
	
