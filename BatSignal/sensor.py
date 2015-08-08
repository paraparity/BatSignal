import pyaudio
import speech_recognition
import threading
import time
import sys
import json
import socket
import queue
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
		self.RATE = int(deviceInfo['defaultSampleRate'])
		self.CHANNELS = 1

		apiInfo = self.audio.get_host_api_info_by_index(deviceInfo['hostApi'])
		self.device_index = apiInfo['defaultInputDevice']

		self.stream = self.audio.open(
			input = True,
			input_device_index = self.device_index,
			format = self.format,
			rate = self.RATE,
			channels = self.CHANNELS,
			frames_per_buffer = self.CHUNK)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.stream.stop_stream()
		self.stream.close()
		self.stream = None
		self.audio.terminate()

def terminal():
	while True:
		command = input("> ")
		if command == "exit":
			break
		else:
			print("unrecognized command \"{0}\".".format(command))

callback_threads = []
non_daemon_threads = []
join_threads_flag = False

message_queue = queue.Queue()

def send_json(jsonString):
	try:
		# open a socket connection to the control node
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# timeout set to 2 seconds
		s.settimeout(2)
		# address of control node is a predefined static ip currently
		s.connect(("10.0.0.254", 50000))

		#send the message
		s.sendall(bytes(jsonString, 'UTF-8'))

		# close the connection
		s.close()

	except Exception as e:
		print("exception in \"send_json\": {0}".format(str(e)))

def threaded_send():
	try:
		while not join_threads_flag:
			while not message_queue.empty():
				send_json(message_queue.get())
				message_queue.task_done()

	except Exception as e:
		print("exception in \"threaded_send\": {0}".format(str(e)))

def audio_callback(recognizer, audio):
	try:
		# recognize the audio
		audioString = recognizer.recognize(audio)

		# construct message
		timeString = time.strftime("%A, %B %d, %Y %X %p", time.gmtime())
		jsonObject = {"name":socket.gethostname(), "audio":audioString, "time":timeString}
		jsonString = json.dumps(jsonObject, sort_keys=True)

		print("\"{1}\" -> \"{0}\"".format(audioString, timeString))
		# push the message onto the queue
		message_queue.put(jsonString)

	except LookupError:
		pass

	except Exception as e:
		print("exception in \"audio_callback\": {0}".format(str(e)))

def threaded_listen(source, recognizer):
	while not join_threads_flag:
		#sys.stdout.write("listening... ")
		#sys.stdout.flush()
		# listening for input on microphone
		audio = recognizer.listen(source)
		#print("done.")

		global callback_threads
		# join dead threads
		dead_threads = [x for x in callback_threads if not x.is_alive()]
		callback_threads = [x for x in callback_threads if x.is_alive()]

		for thread in dead_threads:
			thread.join()

		if audio:
			callback_thread = threading.Thread(target=audio_callback, args=(recognizer, audio, ))
			callback_thread.start()
			callback_threads.append(callback_thread)

	for thread in callback_threads:
		thread.join()

if __name__ == "__main__":
	with PyAudioSource() as source:
		recognizer = speech_recognition.Recognizer()
		recognizer.adjust_for_ambient_noise(source)

		# listen for audio passively
		non_daemon_threads.append(threading.Thread(target=threaded_listen, args=(source, recognizer, )))
		# send information to control node
		non_daemon_threads.append(threading.Thread(target=threaded_send))

		# start worker threads
		for thread in non_daemon_threads:
			thread.start()

		try:
			# call the simple terminal function
			# warning: blocking call
			terminal()

		except KeyboardInterrupt:
			pass

		sys.stdout.write("shutting down...")
		sys.stdout.flush()

		# join all the created threads once their work completes.
		# this can take several seconds.
		join_threads_flag = True
		for thread in non_daemon_threads:
			thread.join()
		message_queue.join()

		print("done.")
