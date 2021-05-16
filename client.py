import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from Protocol import *
from Service import *


def main():
    try:    

        payload="78 32 2d 50 82 b2 c8 53 41 98 fd b8 16 11 a8 b8 6f 8a f8 69 66 38 6c 7c ee 80 c9 21 03 27 8a f7 c0 75 58 9f 9d 69 d2 20 35 30 4e" 
        ps = Service('172.17.0.2')
        packet = ps.createPacket(payload, 5,'172.17.0.2',6000)
        encrypted_packet = ps.encryptPacket(packet)
        ps.sendPacket(encrypted_packet)
        
    except Exception as client_error:
       print('Error: {}'.format(client_error))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[+] Bye!')