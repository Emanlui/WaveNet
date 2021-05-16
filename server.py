import logging
logging.getLogger("scapy.runtime").setLevel(logging.INFO)
from Protocol import *
from Service import *


TCP_IP = '172.17.0.2'
TCP_PORT = 5005
BUFFER_SIZE = 1024  

def main():
    try:    

        ps = Service('172.17.0.2')
        received_packet = ps.receivePacket()
        print(received_packet)
    except Exception as client_error:
       # print(client_error)
       print('Error: {}'.format(client_error))
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[+] Bye!')