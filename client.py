import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from CPPM import *
from Service import *
from keys import *

def client():

	if(openKeys()):
		print("Reading keys")
	else:
		print("Creating keys...")
		generate_keypair()
	if(verifyKeys() == False):
		print("There was an error reading the keys")
		exit(0)
	print("Sending packet...")

	try:    

		payload="Este texto es cifrado" 
		payload = encrypt(payload)
		ps = Service('127.0.0.1')
		packet = ps.createPacket(payload, 5,'127.0.0.1',6000)
		#packet.show()
		ps.sendPacket(packet)
		
	except Exception as client_error:
	   print('Error: {}'.format(client_error))

if __name__ == '__main__':
		
	client()