'''
	This class contains
	the methods related
	to audio managing of
	a sound file
	Parameters: audioFile as the name of the file
				extension in case of extension-sensitive systems
	Note: the audio file must exists within the folder
	of this class
'''
class Sound:

	def __init__(object, audioFile,extension):
		try:
			object.audioFile = audioFile
			object.extension = extension
			object.fullName = audioFile+"."+extension
		except:
			print("Audio File Not Found: ",audioFile)

	'''
	Parameters: the audio file name, contained
	within the folder of the proyect
	'''
	def decodeAudio(object):

		with open(object.fullName, "rb") as fd:
			contents = fd.read()

		if (contents != None):
			print("Audio Found and decoded!")
			return contents

		else:
			print("Audio Could not be decoded!")


	'''
	Parameters: requires the decoded contents of the audio
	Outs: mp3 formed by the contents received
	'''
	def buildAudio(object, decodedAudio):
		fileName = object.audioFile+"Generated."+object.extension
		file = open(fileName,"w+")
		try:
			file.write(decodedAudio)
			file.close()
		except:
			print("Error: File could not be created or write on!")
			return None

		print("AudioFile successfully generated!")


'''
Test method with the example of usage of the class
'''
def test():
	sound = Sound("Sample","mp3")
	decodedAudio = sound.decodeAudio()
	generateFile = sound.buildAudio(decodedAudio)

