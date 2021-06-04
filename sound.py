#python3 -m pip install sounddevice
#sudo apt-get install libportaudio2
import sounddevice as sd

#python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
from scipy.io.wavfile import write 

#this is to import the decode morse library
#Retrieved from https://code.google.com/archive/p/morse-to-text/source/default/source
import Morse.morseToText

#To increase audio volume from an Audio
#pip3 install pydub
#pip3 install ffprobe
#sudo apt-get update  
#sudo apt-get install ffmpeg  
#sudo apt-get install frei0r-plugins  
from pydub import AudioSegment

#To reduce noise from an audio file
#pip3 install noisereduce
# (STILL NOT WORKING)
#Retrieved from: https://github.com/timsainb/noisereduce
#import noisereduce as nr

import numpy as np
import scipy as sp
from scipy.io.wavfile import read
from scipy import signal


#UNIT PERIOD 0.3
#FREQUENCY 500
#SPACE IS |


'''
Parameters: audio file name
this method reduces the noise from
an audio file
'''
def noiseReduce(codeFile):
	print("called noice reduce")
	'''
	# load data
	rate, data = wavfile.read("mywav.wav")
	# select section of data that is noise
	noisy_part = data[10000:15000]
	# perform noise reduction
	reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)
	'''
	(Frequency, array) = read("output.wav")	
	

	FourierTransformation = sp.fft(array) # Calculating the fourier transformation of the signal

	GuassianNoise = np.random.rand(len(FourierTransformation)) # Adding guassian Noise to the signal.
	#print("GuassianNoise "+str(GuassianNoise))

	#NewSound = sum(GuassianNoise, array)
	NewSound = GuassianNoise
	b,a = signal.butter(5, 1000/(Frequency/2), btype='highpass') 
	filteredSignal = signal.lfilter(b,a,NewSound)

	c,d = signal.butter(5, 380/(Frequency/2), btype='lowpass') # ButterWorth low-filter
	newFilteredSignal = signal.lfilter(c,d,filteredSignal) # Applying the filter to the signal

	write("NewFilteredOutput.wav", Frequency, newFilteredSignal) # Saving it to the file.


'''
Parameters: audio file name
this method increases the volume of a 
audio file by 50db
'''
def increase_Volume(codeFile):

	song = AudioSegment.from_wav(codeFile)

	# increase volume by 50 dB
	song = song + 50

	# save the output
	song.export("output.wav", "wav")


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

	'''
	Parameters: (int) recording time
	this methods record during the time given
	and creates an audio file
	'''
	def recordAudio(object, seconds):

		fs = 44100  # Sample rate

		myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
		print("Se ha empezado a grabar audio durante "+str(seconds)+" segundos")
		sd.wait()  # Wait until recording is finished
		write('output.wav', fs, myrecording)  # Save as WAV file 

		print("Se ha terminado la grabacion")

	'''
	Parameters: the audio file name, contained
	within the folder of the proyect
	'''
	def decodeAudio(object):
		
		
		codefile_wav = "output.wav"

		increase_Volume("output.wav")
		

		#noiseReduce(codefile_wav)


		the_file = Morse.morseToText.SoundFile(codefile_wav)
		#the_file = SoundFile("wikipedia.wav")
		the_file.saveplot("original")

		the_filter = Morse.morseToText.SignalFilter()
		the_filter.filter(the_file)
		#the_file.saveas("filtered.wav")

		analyzer = Morse.morseToText.SpectreAnalyzer()
		pulses = analyzer.findpulses(the_file)

		pul_translator = Morse.morseToText.PulsesTranslator()
		code_string = pul_translator.tostring(pulses)

		str_translator = Morse.morseToText.StringTranslator()
		s = str_translator.totext(code_string)

		print(code_string)


		fileName = "output.txt"
		file = open(fileName,"w+")
		try:
			file.write(s)
			file.close()
		except:
			print("Error: File could not be created or write on!")
			return None

		print("Audio Content successfully written on output.txt!")
		print(s)

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
	sound = Sound()
	#sound.recordAudio(54)
	decodedAudio = sound.decodeAudio()
	#generateFile = sound.buildAudio(decodedAudio)


test()