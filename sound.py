'''
PulseAudio and Pavucontrol must be installed in order to record
the audio coming from the terminals and so, record the morse message
emitted through Discord, Zoom or any other app 
(it will not record from microphone until changed)

$ sudo apt install pulseaudio
$ sudo apt install pavucontrol
'''


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
from pydub.playback import play

#pip install playsound
from playsound import playsound


#To reduce noise from an audio file
#pip3 install noisereduce
# (STILL NOT WORKING)
#Retrieved from: https://github.com/timsainb/noisereduce
#import noisereduce as nr

import numpy as np
import scipy as sp
from scipy.io.wavfile import read
from scipy import signal

import time
import os.path


#UNIT PERIOD 0.3
#FREQUENCY 500
#SPACE IS | 
#Wave form: Sinus


MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}


def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
  
            # Looks up the dictionary and adds the
            # correspponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += '|'
  
    return cipher



'''
Parameters: audio file name
this method reduces the noise from
an audio file

def noiseReduce(codeFile):
	print("called noice reduce")
	
	# load data
	#rate, data = wavfile.read("mywav.wav")
	# select section of data that is noise
	#noisy_part = data[10000:15000]
	# perform noise reduction
	#reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)
	
	(Frequency, array) = read(codeFile)	
	

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

'''
Parameters: audio file name
this method increases the volume of a 
audio file by 50db
'''
def increase_Volume(codeFile):

	song = AudioSegment.from_wav(codeFile)

	# increase volume by in dB
	song = song + 25

	# save the output
	song.export(codeFile, "wav")


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
		'''
		if you are not able to record desktop audio:
		Check with sd.query_devices() method
		the device that records your computer audio
		and set the index into sd.default.device
		'''
		#print("Inputs: ",sd.query_devices())
		#python3 -m sounddevice
		sd.default.device = 1
		
		print("Grabando en 3...")
		time.sleep(1)
		print("Grabando en 2...")
		time.sleep(1)
		print("Grabando en 1...")
		time.sleep(1)
		print("Se ha empezado a grabar audio durante "+str(seconds)+" segundos")
		myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
		
		sd.wait()  # Wait until recording is finished
		
		write('output.wav', fs, myrecording)  # Save as WAV file 

		print("Se ha terminado la grabacion \n(Guardado en: output.wav)")

	'''
	Parameters: the audio file name, contained
	within the folder of the proyect
	'''
	def decodeAudio(object):
		codefile_wav = ""
		#flexibility to analize morse files
		loop = True
		while(loop):
			option = input("Archivos para decodificar: \n 1) output.wav \n 2) emmitedMessage.wav \n 3) Personalizado \n")
			if option == "1":
				codefile_wav = "output.wav"
				loop = False
			elif (option == "2"):
				codefile_wav = "emittedMessage.wav"
				loop = False
			else:
				
				codefile_wav = input("Ingrese el nombre del archivo (con su respectiva extension, ejm: test.wav)\n")
				if (os.path.isfile(codefile_wav)):
					loop = False
				else:
					print("Archivo No Encontrado: ",codefile_wav," Por Favor Intente de nuevo\n")
			

		#increase_Volume(codefile_wav) #use this if the code throws null pointer exception, could be due to low audio

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
	def buildAudio(object, message):

		dotDashPause = int(0.3*1000) #ms (0.3 unit period)
		
		encyptedMessage = encrypt(message)
		print("Encrypted message> ",encyptedMessage)

		str_translator = Morse.morseToText.StringTranslator()
		s = str_translator.totext(encyptedMessage)

		print("Translation> ",s)


		#this is the pause after each dot and dash
		pause = AudioSegment.from_wav('silence.wav')
		pause = pause[:dotDashPause] #records only the dotPause miliseconds of the audio


		sound = AudioSegment.from_wav('silence.wav')
		playlist = sound[:0]

		#due to translation, an annoying space at the end was bugging, we delete it
		encyptedMessage = encyptedMessage[:len(encyptedMessage)-1]

		for element in encyptedMessage:

			if element == '.':
				print("DOT")
				sound2 = AudioSegment.from_wav('dot.wav')
				playlist = playlist.append(sound2, crossfade=0)			
				playlist = playlist.append(pause,crossfade=0)
				play(sound2)
				play(pause)
				
			elif element == '-':
				print("DASH")
				sound2 = AudioSegment.from_wav('dash.wav') 
				playlist = playlist.append(sound2,crossfade=0)
				playlist = playlist.append(pause,crossfade=0)
				play(sound2)
				play(pause)
				
			#split between letters when space ' ' is found
			elif element == ' ':
				print("SPACE")
				spacePause = AudioSegment.from_wav('spacePause.wav')
				newPause = spacePause[:600]
				playlist = playlist.append(newPause,crossfade=0)
				playlist = playlist.append(pause,crossfade=0)
				play(spacePause)
				play(pause)	

			#split between words			
			elif element == '|':
				print("TAB")
				tabPause = AudioSegment.from_wav('silence.wav')
				tabPause = sound2[:spacePause]
				playlist = playlist.append(tabPause,crossfade=0)
				play(tabPause)
			

			
		#Save audio file
		with open("emittedMessage.wav", 'wb') as out_f:
			playlist.export(out_f, format='wav')

		print("Emitted Message successfully generated! (emittedMessage.wav)")



'''
menu method with the options of usage of the class
'''
def menu():
	sound = Sound()
	print("Cliente de Sonido!\nSelecciones una opcion:")
	option = input(" 1) Emitir Mensaje \n 2) Grabar Mensaje\n 3) Decodificar Mensaje\n")
	if option == '1':
		message = input("Mensaje a encriptar: ").upper()
		sound.buildAudio(message)
	elif option == '2':
		duration = int(input("Duracion a grabar: "))
		sound.recordAudio(duration)
		decodedAudio = sound.decodeAudio()
	elif option == '3':
		sound.decodeAudio()

test()

menu()