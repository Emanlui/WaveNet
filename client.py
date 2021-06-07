import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from CPPM import *
from Service import *
from keys import *
import keys
import json
import base64
import sys
import threading

BUFFER_SIZE = 1024  
LIST_OF_HOST = []

def sendDataToserver(ip, port, srv_ip, srv_port):

	pub = ""		

	with open('.ssh/id_rsa.pub', mode='rb') as pubk:
		
		pub = pubk.read()
	pub = pub.decode().split("\n")
	msg = "JOIN " + ip + "|" + sys.argv[5] + "|" + port  + "|" + pub[1]+pub[2]
	ps = Service() 
	packet = ps.createPacket(msg, 1, srv_ip, int(srv_port),1)
	packet.show()
	ps.sendPacket(packet,srv_ip, srv_port)

def readPacket(received_packet):
	
	print(received_packet.message)

def listenPacket():

	my_ip = sys.argv[1]
	my_port = sys.argv[2]

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((my_ip, int(my_port)))
	s.listen(1)

	while True:
	  
		conn, addr = s.accept()

		print('Connection address: {}'.format(addr))
		try:

			data = conn.recv(BUFFER_SIZE)
			if data:
				print("SE RECIBIO ALGO")
				packet = IP(data)
				received_packet = packet.getlayer(CPPM)
				received_packet.show()
				readPacket(received_packet)

			else:
				pass
		except Exception as server_error:
			#print(server_error)
			print('Error: {}'.format(server_error))
			conn.close()


def sendPacket():

	while(True):	
		try:  
	
			print("Mi mensaje:")
		   
			my_msg = input()	
			print("Ip de dest:")
			ip_dst = input()
			print("Port de dest:")
			port_dst = input()

			my_msg = ip_dst + "\n" + port_dst + "\n" +	my_msg

			ps = Service() 
			packet = ps.createPacket(my_msg, 1, sys.argv[3], int(sys.argv[4]),0)
			#packet.show()
			ps.sendPacket(packet, sys.argv[3], int(sys.argv[4]))
			
			if my_msg.find("QUIT") != -1:
				sys.exit()
		
		except Exception as client_error:
				#print(client_error)
				print('Error: {}'.format(client_error))

def client():

	my_ip = sys.argv[1]
	my_port = sys.argv[2]
	srv_ip = sys.argv[3]
	srv_port = sys.argv[4]

	if(keys.openKeys()):
		print("Reading keys")
	else:
		print("Creating keys...")
		keys.generate_keypair()
	if(keys.verifyKeys() == False):
		print("There was an error reading the keys")
		exit(0)
	
	sendDataToserver(my_ip, my_port, srv_ip, srv_port)
	
	threads = list()

	t1 = threading.Thread(target=listenPacket, args=())
	t2 = threading.Thread(target=sendPacket, args=())
	
	threads.append(t1)
	threads.append(t2)
	
	t1.start()
	t2.start()
	
	for i in threads:
		i.join()

if __name__ == '__main__':

	client()	
  
	


