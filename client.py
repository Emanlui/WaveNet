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

	sendDataToserver(my_ip, my_port, srv_ip, srv_port)

	while(True):	
		try:  
	
            print("Mi mensaje:")
           
            my_msg = input()	
            print("Ip de dest:")
            ip_dst = input()

            ps = Service() 
            packet = ps.createPacket(my_msg, 1, ip_dst, int(port_dst),0)
            packet.show()
            ps.sendPacket(packet, srv_ip, int(srv_port))
        
        except Exception as client_error:
                print(client_error)
                print('Error: {}'.format(client_error))

if __name__ == '__main__':

	client()	
  
	


