import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from CPPM import *
from Service import *
from keys import *
import keys
import json


LIST_OF_HOST = []
def getHost():

	global LIST_OF_HOST
	
	with open('host.routes', mode='rb') as f:

		for line in f:
			data = line.decode('UTF-8').split('|')
			ip = data[0]
			hostname = data[1]
			port = data[2]
			key = data[3]
			LIST_OF_HOST.append({"ip":ip,"hostname":hostname,"port":int(port),"key":key})
	

def choosingRoute(hops):

    tmp_list = []

    while(hops):
        index = random.randint(0,len(LIST_OF_HOST)-1)	
	
        if(LIST_OF_HOST[index]["ip"] not in tmp_list):

            tmp_list.append([LIST_OF_HOST[index]["key"], LIST_OF_HOST[index]["ip"]])
            hops = hops - 1
            #print(LIST_OF_HOST[index]["key"])
     
    return tmp_list

    

def client():

	if(keys.openKeys()):
		print("Reading keys")
	else:
		print("Creating keys...")
		keys.generate_keypair()
	if(keys.verifyKeys() == False):
		print("There was an error reading the keys")
		exit(0)

	try:    
            
            encrypt_keys_ip = choosingRoute(2)
            encrypt_keys_ip = encrypt_keys_ip[::-1]
            payload="Este texto es cifrado" 
            payload = encrypt(payload)
            print(payload)
            ps = Service('127.0.0.1')
            packet = ps.encryptPacketWithKeysList(payload, encrypt_keys_ip)
            keys_rev = encrypt_keys_ip[::-1]

            packet.show()
        
            #node 1
            node1 = ps.decryptPacket(packet, ps.getKey(keys_rev[0][0]))
            node1.show()
            payload_encrypted = node1.getlayer(CPPM).sprintf("%message%")
            a = IP(bytes(payload_encrypted))
            b = ps.decryptPacket(packet, ps.getKey(keys_rev[0][0]))
            #b = IP(raw(a.encode()))
            #a.show()
            #node1 = ps.createPacket(node1.getlayer(CPPM).sprintf("%message%"), 3, node1.getlayer(IP).sprintf("%dst%"), 6000)
            #node1.show()
            
            #node2
            
            
            #node2 = ps.decryptPacket(a, ps.getKey(keys_rev[1][0]))
            #node2.show()
            #packet.show()
            #ps.sendPacket(packet)
		
	except Exception as client_error:
            print(client_error)
            print('Error: {}'.format(client_error))

if __name__ == '__main__':
   getHost()
   #choosingRoute(3)
   client()

