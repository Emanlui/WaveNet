import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from Protocol import *

# SOCKET SETTINGS
############################################################
TCP_IP = '172.17.0.2'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
############################################################

# NAMES TO SEND INSIDE THE RESPONSE
############################################################
SERVER_NAMES = {
    "1": "Serv1",
    "2": "Serv2",
    "3": "Serv3",
    "4": "Serv4"
}
############################################################


# FUNCTION TO RETURN THE NAME
############################################################
def get_the_name(layer):
    return_name = SERVER_NAMES[layer.sprintf("%name_number%")]
    return return_name
############################################################

# DICTIONARY WITH THE POSSIBLES ACTIONS
############################################################
actions = {
    "get_the_name": get_the_name,
}
############################################################


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    s.settimeout(100)
    while 1:
        conn, addr = s.accept()
        print('Connection address: {}'.format(addr))
        try:
            data = conn.recv(BUFFER_SIZE)
            if data:
                received_packet = Ether() / IP() / TCP() / Protocol(data)
                required_name = actions[received_packet.getlayer("Protocol").sprintf("%service%")] \
                    (received_packet.getlayer("ProtocolRequest"))
                print(received_packet.show())
                print(required_name)
            #packet_to_send = str(Protocol(direction=1, service=1) / ProtocolResponse(own_name=required_name))
            #conn.sendall(packet_to_send)
            else:
                pass
        except Exception as server_error:
            #print(server_error)
            print('Error: {}'.format(server_error))
            conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[+] Bye!')