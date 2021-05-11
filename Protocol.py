from scapy.all import *
from scapy.fields import *
from scapy.layers.inet import IP,TCP


class ProtocolRequest(Packet):
    name = "ProtocolRequest"
    fields_desc = [
        ByteField("name_number", None)
    ]


class ProtocolResponse(Packet):
    name = "ProtocolResponse"
    fields_desc = [
        StrField("own_name", None, fmt="H")
    ]

    def answers(self, other):
        return isinstance(other, ProtocolResponse)


class Protocol(Packet):
    name = "Protocol"
    SERVICE_CODES = {
        0x01: "get_the_name"
    }

    DIRECTIONS = {
        0x00: "Request",
        0x01: "Response"
    }

    fields_desc = [
        ByteEnumField("direction", None, DIRECTIONS),
        ByteEnumField("service", None, SERVICE_CODES),
    ]

bind_layers(Protocol, ProtocolRequest, direction=0x00, service=0x01)
bind_layers(Protocol, ProtocolResponse, direction=0x01, service=0x01)
