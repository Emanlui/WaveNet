from scapy.all import *
from scapy.fields import *
from scapy.layers.inet import IP,TCP
from CPPM import *
import re as regex

class Service():
    
    def __init__(self, tcp_ip=None, tcp_dport = 5005, buffer_size = 1024):
        self.TCP_IP = tcp_ip
        self.TCP_DPORT = tcp_dport 
        self.BUFFER_SIZE = buffer_size 
      
    def encryptPacket(self, packet, key):
        sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=str(key).encode()) 
        return sa.encrypt(packet)

    def decryptPacket(self, packet, key):
        sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=str(key).encode()) 
        return sa.decrypt(packet)
    
    def getKey(self, key_string):
        res = re.search('PublicKey\((.+?)\,', key_string)
        return res.group(1)
        
    def createPacket(self, payload, ver, dst_ip, port, shake):
        packet_to_send = IP(dst=dst_ip)
        packet_to_send /= TCP(dport=port)
        packet_to_send /= CPPM(message=payload, messageLength=len(payload), version=ver, handshake=shake)
        packet_to_send = IP(raw(packet_to_send))
        return packet_to_send
    
    def sendPacket(self, packet, ip, port):
        try:    

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            socketsr1 = StreamSocket(s, CPPM)
            
            ans = socketsr1.sr1(packet, timeout=2, verbose=False)
            s.close()
        
        except Exception as client_error:
            print('Error: {}'.format(client_error))
      
    def packetToBytes(self, packet):
        return raw(packet)
    def bytesToPacket(self, packet):
        return CPPM(packet)
    def receivePacket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.TCP_IP, self.TCP_DPORT))
        s.listen(1)
        s.settimeout(100)
        while True:
            conn, addr = s.accept()
            print('Connection address: {}'.format(addr))
            try:
                data = conn.recv(self.BUFFER_SIZE)
                if data:
                    packet = IP(data)
                    received_packet = CPPM(packet.getlayer(Raw).load)
                    received_packet.show()
                    #return received_packet
    
                else:
                    pass
            except Exception as server_error:
                #print(server_error)
                print('Error: {}'.format(server_error))
                conn.close()
