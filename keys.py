import uuid
from base64 import b64encode

import socket
from OpenSSL import SSL, crypto
import rsa 

PRIVATE_KEY = ""
PUBLIC_KEY = ""

def openKeys():

	global PRIVATE_KEY
	global PUBLIC_KEY
	
	try:
		with open('.ssh/id_rsa.priv', mode='rb') as privk:
			
			PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(privk.read())

		with open('.ssh/id_rsa.pub', mode='rb') as pubk:
			
			PUBLIC_KEY = rsa.PublicKey.load_pkcs1(pubk.read())
	except Exception:
		return False
	return True

def createFileKeys(private, public):

	pri = private.save_pkcs1('PEM').decode()

	with open (".ssh/id_rsa.priv", "w") as prv_file:
		prv_file.write(pri)
		prv_file.close()

	pub = public.save_pkcs1('PEM').decode()

	with open (".ssh/id_rsa.pub", "w") as pub_file:
		pub_file.write(pub)
		pub_file.close()



def generate_keypair():

	publicKey, privateKey = rsa.newkeys(512)

	createFileKeys(privateKey,publicKey)

	global PRIVATE_KEY
	global PUBLIC_KEY

	PRIVATE_KEY = privateKey
	PUBLIC_KEY = publicKey

	return privateKey, publicKey

def verifyKeys():

	try:
		# create a message
		message = 'This is a test'
		encrypt_message = encryptMyPacket(message)
		decrypt_message = decryptMyPacket(encrypt_message)
		if(message == decrypt_message):
			return True
		else:
			return False

	except Exception:
		return False
	return True

def decryptMyPacket(message):
	
	newMessage = rsa.decrypt(message, PRIVATE_KEY).decode()	  
	return newMessage

def encryptMyPacket(message):

	newMessage = rsa.encrypt(message.encode(),PUBLIC_KEY)
	return newMessage

def encrypt(message, pub_key):
	#print(pub_key)
	pub_key = "-----BEGIN RSA PUBLIC KEY-----\n" + "MEgCQQCNTEZfTmzuTOxRUVELgHn2L4icNlrsVWYewO+IN0G0bNkH5GEOtSWKA6tNKXy/X8J8xLgyjezv9dpi0g2nssszAgMBAAE=" + "\n-----END RSA PUBLIC KEY-----\n"
	
	#print(pub_key)

	PUBLIC_KEY = rsa.PublicKey.load_pkcs1(pub_key)
	#newMessage = rsa.encrypt(message.encode(),pub_key)
	return message
