from scapy.all import *
from scapy.fields import *
from scapy.layers.inet import IP,TCP
import struct

class CPPM(Packet):
    #Communication Protocol Packet Manager
    name = "CPPM"

    fields_desc = [
        LenField('messageLength', 0, fmt="H"),
        ShortField("chksum", None),
        ShortField("version", 1),
        ShortField("handshake", 0),
        StrField("message", "")
    ]
    
    def validateChecksum(self, packet):
        packet_chksum = packet.chksum
        packet.chksum = 0
        packet_bytes = raw(packet)
        packet.chksum = packet_chksum
        return checksum(packet_bytes) == packet_chksum
    
    def setCheksum(self, packet):
        packet.chksum = 0
        packet_bytes = raw(packet)
        packet.chksum = checksum(packet_bytes)
        return packet
       
        
bind_layers(TCP, CPPM)