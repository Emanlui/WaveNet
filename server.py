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
import base64
#import sound

BUFFER_SIZE = 4096  

LIST_OF_HOST = []

def resendToHost(received_packet):

	received_packet.show()
	
	msg = received_packet.message.decode().split("\n")

	validation = False

	print(LIST_OF_HOST)

	try:
		for i in LIST_OF_HOST:
			if(i[0] == msg[0] and i[2] == int(msg[1])):
				validation = True
				break
	except:
		pass

	if(validation == False):
		print("Validation error.")
	else:
		print("CREANDO PAQUETE")
		ps = Service() 
		packet = ps.createPacket(received_packet.message.decode(), 1, msg[0], int(msg[1]),0)
		#packet.show()
		ps.sendPacket(packet, msg[0], int(msg[1]))

def getHostData(ip, port):
	
	global LIST_OF_HOST
	

	for i in LIST_OF_HOST:
		if(str(i[0]) == str(ip) and int(i[2]) == int(port)):
			return i
	return None

def createPacket(msg, destination_ip, destination_port, key):

	msg = msg.split("\n")
	getHost()
	hops = choosingRoute(1)
	msg1 = keys.encrypt(msg[2], key)
	msg1 = str(destination_ip)+"\n"+str(destination_port)+"\n" + str(base64.b64encode(msg1).decode("utf-8"))
	l = msg1[:70]
	r = msg1[70:]
	print(l)
	print(r)
	msg2 = ""
	for i in hops:
		msg2 = keys.encrypt(l, i[2])
		msg2 = str(i[0])+"\n"+str(i[1])+"\n" + base64.b64encode(msg2).decode("utf-8") + r
		l = msg2[:70]
		r = msg2[70:]
		print(l)
		print(r)
	return msg2, hops 


def getHost():

	global LIST_OF_HOST
	LIST_OF_HOST = []
	with open('host.txt', mode='rb') as f:

		for line in f:
			data = line.decode("utf-8").split('|')
			ip = data[0]
			hostname = data[1]
			port = data[2]
			key = data[3]
			LIST_OF_HOST.append([ip,hostname,int(port),key])


def choosingRoute(hops):

	tmp_list = []
	global LIST_OF_HOST
	while(hops):
		index = random.randint(0,len(LIST_OF_HOST)-1)	
		if(LIST_OF_HOST[index][0] not in tmp_list):
			host = [LIST_OF_HOST[index][0], LIST_OF_HOST[index][2],LIST_OF_HOST[index][3]]
			tmp_list.append(host)
			hops = hops - 1
	
	
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
							with open("host.txt", "a") as f:
								f.write(received_packet.message.decode() + "\n")
								f.close()
								
							getHost()
						elif(received_packet.handshake == 2):
							getHost()

							dst_port = received_packet.message.decode().split("\n")[1]
							my_msg,hops = createPacket(received_packet.message.decode(), packet[IP].dst, dst_port, getHostData(packet[IP].dst, dst_port)[3])

							ps = Service() 
							packet = ps.createPacket(my_msg, 1, hops[len(hops)-1][0], int(hops[len(hops)-1][1]),0)

							ps.sendPacket(packet, hops[len(hops)-1][0], int(hops[len(hops)-1][1]))

						else:
							resendToHost(received_packet)
					else:
						pass
				except Exception as server_error:
					print(server_error)
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

	with open("routes.txt", "w") as f:
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




