import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.INFO)
from CPPM import *
from Service import *
from keys import *

BUFFER_SIZE = 1024  

LIST_OF_HOST = []

#def choosingRoute():
	

#def sendKeys():

def server():
	
	if(openKeys()):
		print("Reading keys")
	else:
		print("Creating keys...")
		generate_keypair()
	if(verifyKeys() == False):
		print("There was an error reading the keys")
		exit(0)
	print("Server is running...")
	try:    
		
		#sendKeys()
		ps = Service('127.0.0.1')
	
		received_packet = ps.receivePacket()
		print(decrypt(received_packet))
	
	except Exception as client_error:

	   print('Error: {}'.format(client_error))

if __name__ == '__main__':
		
	server()