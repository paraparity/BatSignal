import threading
import socket
import json
import queue
import time
import select

force_thread_join = False

def work(queue):
	try:
		while not force_thread_join:
			while not queue.empty():
				jsonMessage = queue.get()
				queue.task_done()

	except Exception as e:
		print("Worker thread error: {0}!".format(str(e)))

def listen(queue):
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# (localhost, port:50000)
		server.bind(('', 50000))

		# backlog (system dependent value)
		server.listen(5)

		read_list = [server]
		while not force_thread_join:
			readable, writeable, errored = select.select(read_list, [], [], 0)
			for s in readable:
				if s is server:
					client, address = server.accept()
					read_list.append(client)
					print("Connection from {0}.".format(address))
				else:
					data = ''

					packet = s.recv(1024)
					while packet:
						data += packet
						packet = s.recv(1024)

					queue.put(json.loads(data))
					client.close()
					read_list.remove(s)

		server.close()

	except Exception as e:
		print("Listener thread error: {0}!".format(str(e)))

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

if __name__ == "__main__":
	threads = []
	messageQueue = queue.Queue()

	try:
		# perform initial configuration
		configure()

		# spin up listener and work threads
		threads.append(threading.Thread(target=listen, args=(messageQueue, )))
		threads.append(threading.Thread(target=work, args=(messageQueue, )))

		for thread in threads:
			thread.start()

		# simple terminal emulator
		# warning: blocking function call
		terminal()

	except KeyboardInterrupt:
		pass

	except Exception as e:
		print("Error: {0}".format(str(e)))

	force_thread_join = True

	# join queue and threads
	messageQueue.join()
	for thread in threads:
		thread.join()

