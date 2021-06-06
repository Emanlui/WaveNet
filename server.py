import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.INFO)
from CPPM import *
from Service import *
import keys
import socket
import threading
import uuid
import requests
import random
import os
from time import sleep
import IRC
#import sound

BUFFER_SIZE = 1024  

LIST_OF_HOST = []

def getHostData(ip):
	
	for i in LIST_OF_HOST:
		if(i['ip'] == ip):
			return i
	return Null

def createPacket(msg, destination_ip, destination_port, key, ip):
	
	getHost()
	hops = choosingRoute(2, ip)
	
	#print(hops)
	
	msg1 = encrypt(base64.b64encode(msg.encode("utf-8")), key)
	msg1 = str(destination_ip)+"\n"+str(destination_port)+"\n" + msg1.decode("utf-8")

	#print(msg1)

	msg2 = encrypt(base64.b64encode(msg1.encode("utf-8")), hops[0][2])
	msg2 = str(hops[0][0])+"\n"+str(hops[0][1])+"\n" + msg2.decode("utf-8")
	
	#print(msg2)

	msg3 = encrypt(base64.b64encode(msg2.encode("utf-8")), hops[1][2])
	msg3 = str(hops[1][0])+"\n"+str(hops[1][1])+"\n" + msg3.decode("utf-8")
	#print(msg3)
	return msg3 



def getHost():

	global LIST_OF_HOST
	
	with open('host.txt', mode='rb') as f:

		for index,line in f:
			if(index != 0):
				data = line.decode('UTF-8').split('|')
				ip = data[0]
				hostname = data[1]
				port = data[2]
				key = data[3]
				LIST_OF_HOST.append({"ip":ip,"hostname":hostname,"port":int(port),"key":key})
	

def choosingRoute(hops, ip):

	tmp_list = []

	while(hops):
		index = random.randint(0,len(LIST_OF_HOST)-1)	
	
		if(LIST_OF_HOST[index]["ip"] not in tmp_list and ip != LIST_OF_HOST[index]["ip"]):
			host = [LIST_OF_HOST[index]["ip"], LIST_OF_HOST[index]["port"],LIST_OF_HOST[index]["key"]]
			tmp_list.append(host)
			hops = hops - 1
			#print(LIST_OF_HOST[in`dex]["key"])
	 
	return tmp_list

def listenForMessage(filename):
	try:
		file = open(filename, "rb")
		data = file.read()
		file.close()
		if(len(data)>0):
			file = open(filename, "w")
			file.truncate()
			file.close()   
		   
			return data    
		else:
			return False
	except IOError as e:
		print(e)
		return False
	
def joinMessageBytes(message_chunks):
	return b''.join(message_chunks)
	
def chunkMessage(message, chunk_size):
	chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
	return chunks

def sendKeys(ip, port):
	
	key = ""
	try:
		with open('.ssh/id_rsa.pub', mode='rb') as pubk:
			
			key = pubk.read()
	except Exception:
		print("error")
	return key

def sendMessageIRC(msg):

	#sleep(3)

	#print(len(LIST_OF_HOST), "NUMERO DE HOSTS")
	
	#for i in LIST_OF_HOST:
		#bot.sendMessageIRC(i)
	IRC.sendMessageIRC(msg)

def threatListen():

	my_ip = sys.argv[1]
	my_port = sys.argv[2]


	try:    
	   
			#ps = Service(my_ip, int(my_port))
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((my_ip, int(my_port)))
			s.listen(1)
			#s.settimeout(100)

			while True:
			  
				conn, addr = s.accept()

				print('Connection address: {}'.format(addr))
				try:

					data = conn.recv(BUFFER_SIZE)
					if data:
						packet = IP(data)
						received_packet = packet.getlayer(CPPM)
						#received_packet.show()
		
						if(received_packet.handshake == 1):
							# Recien entrando al server.
							with open("host.txt", "a") as f:
								f.write(received_packet.message.decode().split(" ")[1] + "\n")	
								f.close()
							sendMessageIRC(received_packet.message.decode())
						else:
							sendMessageIRC(received_packet.message.decode())
					else:
						pass
				except Exception as server_error:
					#print(server_error)
					print('Error: {}'.format(server_error))
					conn.close()
			
	
	except Exception as client_error:

		print('Error: {}'.format(client_error))
		print("Escuchar")
		sleep(1)
def escuchar():

	while(1):
		print("Escuchar")
		sleep(1)
	
def hablar():
	while(1):
		print("Hablar")
		sleep(1)

def IRCServer():
	IRC.serverManagment(sys.argv[3])

def server():
	
	with open("host.txt", "w") as f:
		f.write("")	
		f.close()

	threads = list()

	t1 = threading.Thread(target=threatListen, args=())
	#t2 = threading.Thread(target=escuchar, args=())
	#t3 = threading.Thread(target=hablar, args=())
	t4 = threading.Thread(target=IRCServer, args=())

	threads.append(t1)
	#threads.append(t2)
	#threads.append(t3)
	threads.append(t4)

	t1.start()
	#t2.start()
	#t3.start()
	t4.start()

	for i in threads:
		i.join()


if __name__ == '__main__':
		
	server()




