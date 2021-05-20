from scapy.all import *
from scapy.fields import *
from scapy.layers.inet import IP,TCP
from CPPM import *

class Service():
    
    def __init__(self, tcp_ip=None, tcp_dport = 5005, buffer_size = 1024):
        self.TCP_IP = tcp_ip
        self.TCP_DPORT = tcp_dport 
        self.BUFFER_SIZE = buffer_size 
        
    def createPacket(self, payload, ver, dst_ip, port):
        packet_to_send = IP(dst=dst_ip)
        packet_to_send /= TCP(dport=port)
        packet_to_send /= CPPM(message=payload, messageLength=len(payload), version=ver)
        packet_to_send = IP(raw(packet_to_send))
        return packet_to_send
    
    def sendPacket(self, packet):
        try:    
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, self.TCP_DPORT))
            socketsr1 = StreamSocket(s, CPPM)
            ans = socketsr1.sr1(packet, timeout=2, verbose=False)
            s.close()
        
        except Exception as client_error:
            print('Error: {}'.format(client_error))
           
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