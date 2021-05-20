import rsa
import time
import server
import client

import subprocess

def main():
	publicKey, privateKey = rsa.newkeys(1024)
	
	print(type(publicKey))

	subprocess.Popen(['python3', 'server.py', str(privateKey), str(publicKey)])
	subprocess.Popen(['python3', 'client.py',str(privateKey), str(publicKey)])
	

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('[+] Bye!')