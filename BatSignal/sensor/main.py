import pyaudio
import speech_recognition
import threading
import time
import sys

class PyAudioSource(speech_recognition.AudioSource):
	def __init__(self, device_index = None):
		self.format = pyaudio.paInt16
		self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
		self.CHUNK = 1024

		self.audio = None
		self.stream = None

	def __enter__(self):
		self.audio = pyaudio.PyAudio()

		deviceInfo = self.audio.get_default_input_device_info()
		self.RATE = 44100
		self.CHANNELS = 1

		self.stream = self.audio.open(
			input = True,
			input_device_index = None,
			format = self.format,
			rate = self.RATE,
			channels = self.CHANNELS,
			frames_per_buffer = self.CHUNK)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		print("Exiting...")

		self.stream.stop_stream()
		self.stream.close()
		self.stream = None
		self.audio.terminate()

		print("Done.")

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
	print("audio callback started...")

	try:
		audioString = recognizer.recognize(audio)

		# open a socket connection to the control node
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# address of control node is a predefined static ip
		s.connect(("192.168.1.12", 50000))

		# construct message
		timeString = time.gmtime(time.time())
		jsonObject = {"name":"foo", "audio":audioString, "time":timeString}
		jsonString = json.dumps(jsonObject, sort_keys=True)

		print(jsonString)

		# send the message
		s.sendall(jsonString)
		# close the connection
		s.close()
 
	except LookupError:
		print("Error: audio not recognized!")

	print("audo callback finished.")

def adjust_for_noise(recognizer, source):
	recognizer.adjust_for_ambient_noise(source)

class RepeatingTimer(threading.Thread):
	def __init__(self, callback, time = None, args = ()):
		threading.Thread.__init__(self)

		self.callback = callback
		self.time = time
		self.args = args

	def run(self):
		while True:
			self.callback(*self.args)
			if self.time:
				time.sleep(self.time)

if __name__ == "__main__":
	try:
		with PyAudioSource() as source:
			recognizer = speech_recognition.Recognizer()

			# periodically adjust for ambient noise
			noise_adjusting_thread = RepeatingTimer(adjust_for_noise, 15, (recognizer, source, ))
			noise_adjusting_thread.Daemon = True
			noise_adjusting_thread.start()

			# listen for audio passively
			listener_thread = recognizer.listen_in_background(source, audioCallback)

			# call the simple terminal function
			# warning: blocking call
			terminal()
	except KeyboardInterrupt:
		pass

