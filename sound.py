#python3 -m pip install sounddevice
#sudo apt-get install libportaudio2
import sounddevice as sd

#python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
from scipy.io.wavfile import write 

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
	Parameters: (int) recording time
	this methods record during the time given
	and creates an audio file
	'''
	def recordAudio(object, seconds):

		fs = 44100  # Sample rate

		myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
		sd.wait()  # Wait until recording is finished
		write('output.wav', fs, myrecording)  # Save as WAV file 


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
	sound.recordAudio(2)
	#decodedAudio = sound.decodeAudio()
	#generateFile = sound.buildAudio(decodedAudio)


test()