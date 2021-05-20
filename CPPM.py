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
        StrField("message", "")
    ]
    
    def post_build(self, p, pay):
        p += pay
        if(self.chksum == None):
            self.chksum = checksum(p)
        return p 
    