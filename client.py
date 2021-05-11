import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from Protocol import *

# SOCKET SETTINGS
############################################################
TCP_IP = '172.17.0.2'
TCP_DPORT = 5005
BUFFER_SIZE = 1024
SERV = 2
############################################################


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_DPORT))
        socketsr1 = StreamSocket(s, Protocol)
        packet_to_send = Protocol(direction=0, service=1)/ProtocolRequest(name_number=SERV)
        ans = socketsr1.sr1(packet_to_send, timeout=2, verbose=False)
        server_name = ans.getlayer("ProtocolResponse").sprintf("%own_name%")
        print('Server name: {}').format(server_name)
        s.close()
    except Exception as client_error:
        print('Error: {}'.format(client_error))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[+] Bye!')