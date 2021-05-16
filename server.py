import logging
logging.getLogger("scapy.runtime").setLevel(logging.INFO)
from Protocol import *
import libpcap


TCP_IP = '172.17.0.2'
TCP_PORT = 5005
BUFFER_SIZE = 1024  

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
            #packets = sniff(filter="dst port 5005", count=5)   

            if data:

                sa = SecurityAssociation(ESP, spi=0xdeadbeef, crypt_algo='AES-CBC', crypt_key=str('2948404D63516654').encode())
                decrypted_packet = sa.decrypt(IP(data))
                received_packet = CPPM(decrypted_packet.getlayer(Raw).load)
                received_packet.show2()

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