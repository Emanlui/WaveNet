import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.INFO)
from CPPM import *
from Service import *
import keys
import socket
import uuid
import requests
import random

BUFFER_SIZE = 1024  

LIST_OF_HOST = [
{"ip":"1.1.1.1","hostname":'host1',"port":5001,"key":"PublicKey(7643116678661065657748006528602167115152432119762004779898318705572781888326531964564986617115611415905654957575725435793152416799169791009014953465573581, 65537)"},
{"ip":"2.2.2.2","hostname":'host2',"port":5002,"key":"PublicKey(7643116678661065657748006528602167115152432119762004779898318705572781888326531964564986617115611415905654957575725435793152416799169791009014953465573582, 65537)"},
{"ip":"3.3.3.3","hostname":'host3',"port":5003,"key":"PublicKey(7643116678661065657748006528602167115152432119762004779898318705572781888326531964564986617115611415905654957575725435793152416799169791009014953465573583, 65537)"},
{"ip":"4.4.4.4","hostname":'host4',"port":5004,"key":"PublicKey(7643116678661065657748006528602167115152432119762004779898318705572781888326531964564986617115611415905654957575725435793152416799169791009014953465573584, 65537)"}
]

#def sendToNextHop(ip, port, payload):
	
def getHost():

	with open ("host.routes", "w") as f:
		for i in LIST_OF_HOST:
			
			f.write(i["ip"])
			f.write("|")
			f.write(i["hostname"])
			f.write("|")
			f.write(str(i["port"]))
			f.write("|")
			f.write(i["key"])
			f.write("\n")
		f.close()

def sendKeys():
	
	ip = requests.get('http://ip.42.pl/raw').text
	hostname = uuid.uuid4()
	port = 5005
	if(keys.openKeys()):
		print("Reading keys")
	else:
		print("Creating keys...")
		keys.generate_keypair()
	if(keys.verifyKeys() == False):
		print("There was an error reading the keys")
		exit(0)
	
	print(ip)
	print(hostname)
	print(port)
	print(keys.PRIVATE_KEY)
	print(keys.PUBLIC_KEY)

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
		
	#choosingRoute(3)
	getHost()




