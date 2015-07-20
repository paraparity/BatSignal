import pyaudio
import speech_recognition
import threading
import time
import sys
import json
import socket
import queue

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
listening_lock = threading.Lock()

message_queue = queue.Queue()

def send_json(jsonString):
	try:
		# open a socket connection to the control node
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# address of control node is a predefined static ip currently
		s.connect(("192.168.1.12", 50000))

		#send the message
		s.sendall(jsonString)

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
		timeString = time.gmtime(time.time())
		jsonObject = {"name":"foo", "audio":audioString, "time":timeString}
		jsonString = json.dumps(jsonObject, sort_keys=True)

		print(jsonString)
		# push the message onto the queue
		message_queue.put(jsonString)

	except LookupError:
		pass

	except Exception as e:
		print("exception in \"audio_callback\": {0}".format(str(e)))

def adjust_for_noise(recognizer, source):
	listening_lock.acquire()
	try:
		print('adjusting for ambient noise')
		recognizer.adjust_for_ambient_noise(source)
		print('finished adjusting for ambient noise')
	finally:
		listening_lock.release()

class RepeatingTimer(threading.Thread):
	def __init__(self, callback, time = None, args = ()):
		threading.Thread.__init__(self)

		self.callback = callback
		self.time = time
		self.args = args

	def run(self):
		while not join_threads_flag:
			self.callback(*self.args)
			if self.time:
				time.sleep(self.time)

def threaded_listen(source, recognizer):
	while not join_threads_flag:
		audio = None

		listening_lock.acquire()
		try:
			print('listening...')
			# listening for input on microphone
			# times out after 15 seconds of listening
			audio = recognizer.listen(source, 15)
		except Exception as e:
			print("error in threaded_listen: {0}".format(str(e)))
		finally:
			listening_lock.release()
			print('finished listening')

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
		recognizer.dynamic_energy_threshold = True

		adjust_for_noise(recognizer, source)

		# periodically adjust for ambient noise
		non_daemon_threads.append(RepeatingTimer(adjust_for_noise, 15, (recognizer, source, )))
		# listen for audio passively
		non_daemon_threads.append(threading.Thread(target=threaded_listen, args=(source, recognizer, )))
		# send information to control node
		#non_daemon_threads.append(threading.Thread(target=threaded_send))

		# start worker threads
		for thread in non_daemon_threads:
			thread.start()

		try:
			# call the simple terminal function
			# warning: blocking call
			terminal()

		except KeyboardInterrupt:
			pass

		print("Shutting down.")

		# join all the created threads once their work completes.
		# this can take several seconds.
		join_threads_flag = True
		for thread in non_daemon_threads:
			thread.join()
		message_queue.join()

