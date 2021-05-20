import string
import socket
import sys
import os
import random
import time

server = "209.97.147.243"       #settings
channel = b'"#channel1"'
botnick = b'"kmakbot"'
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
irc.connect((server, 6667))                                                       #connects to the server
time.sleep(3)

var = b'"USER "'+ botnick +" "+ botnick +" "+ botnick + b'" :This is a fun bot!\n"'
irc.send(var) #user authentication
time.sleep(3)
irc.send(b'"NICK "'+ botnick +b'"\n"')                            #sets nick
time.sleep(3)
irc.send(b'"JOIN "'+ channel +b'"\n"')        #join the chan

while 1:    #puts it in a loop
    try:
        text=irc.recv(2040)  #receive the text
        print (text)
    except Exception:
        pass
    if text.find(b'"PING"') != -1:
        irc.send(b'"PONG "' + text.split()[1] + b'"\r\n"')
    if text.lower().find(b'":!hi"') != -1:
        irc.send(b'"PRIVMSG "' + channel + b'" :!Hello\r\n"')

input()