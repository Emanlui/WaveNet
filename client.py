import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from Protocol import *
import struct

# SOCKET SETTINGS
############################################################
TCP_IP = '172.17.0.2'
TCP_DPORT = 5005
BUFFER_SIZE = 1024
############################################################


def main():
    try:    
        sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=str('2948404D63516654').encode())
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_DPORT))
        socketsr1 = StreamSocket(s, CPPM)
        payload="78 32 2d 50 82 b2 c8 53 41 98 fd b8 16 11 a8 b8 6f 8a f8 69 66 38 6c 7c ee 80 c9 21 03 27 8a f7 c0 75 58 9f 9d 69 d2 20 35 30 4e" 
    
        packet_to_send = IP(dst='172.17.0.2')
        packet_to_send /= TCP(dport=5005)
        packet_to_send /= CPPM(message=payload, messageLength=213, version=3)
        packet_to_send = IP(raw(p))
        packet_to_send = sa.encrypt(p)
        ans = socketsr1.sr1(packet_to_send, timeout=2, verbose=False)
        s.close()
    except Exception as client_error:
       # print(client_error)
       print('Error: {}'.format(client_error))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[+] Bye!')