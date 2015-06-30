import pyaudio
import speech_recognition
import threading

class PyAudioSource(speech_recognition.AudioSource):
	def __init__(self, device_index = None):
		self.device_index = device_index
		self.format = pyaudio.paInt16
		self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
		self.RATE = 44100
		self.CHANNELS = 1
		self.CHUNK = 1024

		self.audio = None
		self.stream = None

	def __enter__(self):
		self.audio = pyaudio.PyAudio()
		self.stream = self.audio.open(
			input_device_index = self.device_index,
			format = self.format,
			rate = self.RATE,
			channels = self.CHANNELS,
			frames_per_buffer = self.CHUNK,
			input = True)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.stream.stop_stream()
		self.stream.close()
		self.stream = None
		self.audio.terminate()
		self.audio = None

def configure():
	pass

def terminal():
	while True:
		command = input("> ")
		if command == "exit":
			break
		elif command == "reconfigure":
			configure()
		else:
			print("Error: unrecognized command \"{0}\".".format(command))

def audioCallback(recognizer, audio):
	try:
		print("audio: " + recongizer.recognize(audio))
	except LookupError:
		print("Error: audio not recognized!")

class NoiseAdjuster(object):
	def __init__(self, recognizer, source):
		self.recognizer = recognizer
		self.source = source

	def callback(self):
		if not exiting:
			self.recognizer.adjust_for_ambient_noise(self.source)
			threading.Timer(15, self.callback).start()

if __name__ == "__main__":
	speechRecognizer = speech_recognition.Recognizer()
	with PyAudioSource() as source:
		# periodically adjust for ambient noise
		noiseAdjuster = NoiseAdjuster(speechRecognizer, source)
		noiseAdjuster.callback()

		# listen for audio passively
		speechRecognizer.listen_in_background(source, audioCallback)

	# call the simple terminal function
	# warning: blocking call
	terminal()

	print("BatSignal sensor node module shutting down.")
