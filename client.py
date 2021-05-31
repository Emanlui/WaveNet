import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from CPPM import *
from Service import *
from keys import *
import keys
import json
import base64
import sys

LIST_OF_HOST = []

def createPacket(msg, destination_ip, destination_port, key, ip):
	
	getHost()
	hops = choosingRoute(2, ip)
	
	print(hops)
	
	msg1 = encrypt(base64.b64encode(msg.encode("utf-8")), key)
	msg1 = str(destination_ip)+"\n"+str(destination_port)+"\n" + msg1.decode("utf-8")

	print(msg1)

	msg2 = encrypt(base64.b64encode(msg1.encode("utf-8")), hops[0][2])
	msg2 = str(hops[0][0])+"\n"+str(hops[0][1])+"\n" + msg2.decode("utf-8")
	
	print(msg2)

	msg3 = encrypt(base64.b64encode(msg2.encode("utf-8")), hops[1][2])
	msg3 = str(hops[1][0])+"\n"+str(hops[1][1])+"\n" + msg3.decode("utf-8")
	print(msg3)
	return msg3 

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
	

def choosingRoute(hops, ip):

	tmp_list = []

	while(hops):
		index = random.randint(0,len(LIST_OF_HOST)-1)	
	
		if(LIST_OF_HOST[index]["ip"] not in tmp_list and ip != LIST_OF_HOST[index]["ip"]):
			host = [LIST_OF_HOST[index]["ip"], LIST_OF_HOST[index]["port"],LIST_OF_HOST[index]["key"]]
			tmp_list.append(host)
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
			payload="Este texto es cifrado" 
			
			ps = Service('127.0.0.1')
			packet = ps.encryptPacketWithKeysList(payload, encrypt_keys_ip)
			keys_rev = encrypt_keys_ip[::-1]

			packet.show()
			ps.sendPacket(packet)
			
			'''
			
			
			'''

	except Exception as client_error:
			print(client_error)
			print('Error: {}'.format(client_error))

if __name__ == '__main__':

	#client()	
  
	ip = sys.argv[1]
	getHost()

	createPacket("Mi mensaje", ip, 8080, "AAAAB3NzaC1yc2EAAAADAQABAAABgQDYg/fQ1DEJWZUoXx/kV/uaTYdj4lWn8Ch7OY5/UtUQ5Tfcc46up/X7rucVun4QG5XS54hpQ8Vgm/dzF8DETZrvT9bljMsMRk0SWpytegp1sd9OospwKnuL6dafVo41qp6fjpiKlbEtN4OEJ4eKH2mVGlXIqsqQyNgSgQWrSEv8wzm9qGqX5eUadGiI5EvaMo3xFY1amv/ELm5jvBjnGHZUGVrguRQl6Qv0mo5EeBC5KPqOTURfIvq4UjP/hbDcTLfEWCSF/nKM7zPYnyG55Ze4GcstARirbP3moNsh/DlMCdsM6w8p0KR84sSNSja63B7YN36VkzPltL10rS545QWVNuEzeRa4a+WDKBBAnCgyacd3FLEpGWdKtvgDkYbOduF9iRyaT+UEZ6N2MzNVUu6pKywuIIqZAQpqXX7HblYGYh7vUfteWRnrjSoLugX9X/0gfDX/mp+0eMOMDqVmwy5Iz8zYIm6SAIZdruExUs9487vkM/6+OS+9KlSb6hkQ+TU=", ip)

	


