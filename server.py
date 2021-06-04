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
from time import sleep

#import sound

BUFFER_SIZE = 1024  

LIST_OF_HOST = []

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

def sendKeys(ip, port):
	
	key = ""
	try:
		with open('.ssh/id_rsa.pub', mode='rb') as pubk:
			
			key = pubk.read()
	except Exception:
		print("error")
	return key

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

def server():
	
    #if(openKeys()):
     #   print("Reading keys")
    #else:
     #   print("Creating keys...")
      #  generate_keypair()
    #if(verifyKeys() == False):
     #   print("There was an error reading the keys")
      #  exit(0)
       # print("Server is running...")
    try:    
        while(True):
            sleep(0.9000)
            print("Listening messages...")
            message = listenForMessage("SampleGenerated.txt")
            print(message)
            if(message):
                chunked_message = chunkMessage(message, 128)
                for m_bytes in chunked_message:
                    print(m_bytes)
            
        #sendKeys()
		#ps = Service('127.0.0.1')
	
		#received_packet = ps.receivePacket()
		#print(decrypt(received_packet))
	
    except Exception as client_error:

        print('Error: {}'.format(client_error))

if __name__ == '__main__':
		
	#choosingRoute(3)
	#getHost()
    server()




