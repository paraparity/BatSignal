import threading
import socket
import json
import queue
import time
import select
import smtplib
from email.mime.text import MIMEText

# configurable properties
admins = []
control_phrases = []

# worker threads
join_threads_flag = False
message_queue = queue.Queue()
worker_threads = []

email_server = None

def send_email(json_message):
	message_to = ", ".join(admins)
	message_from = "batsignal.noreply@gmail.com"

	message = MIMEText(json_message.dumps())
	message["Subject"] = "Attention required at node {0}".format(json_message["sensor"])
	message["From"] = message_from
	message["To"] = message_to

	email_server.send_mail(message_from, message_to, message)

def threaded_parse():
	def parse(json_message):
		audio = json_message["audio"]
		for phrase in control_phrases:
			if audio.find(phrase) >= 0:
				send_email(json_message)
				break

	try:
		while not join_threads_flag:
			while not message_queue.empty():
				parse(message_queue.get())
				message_queue.task_done()

	except Exception as e:
		print("exception in \"threaded_parse\": {0}!".format(str(e)))

def threaded_listen():
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# (localhost, port:50000)
		server.bind(('', 50000))

		# backlog (system dependent value)
		server.listen(5)

		read_list = [server]
		while not join_threads_flag:
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

					message_queue.put(json.loads(data))
					client.close()
					read_list.remove(s)

		server.close()

	except Exception as e:
		print("exception in \"threaded_listen\": {0}!".format(str(e)))

def configure():
	try:
		global admins
		global control_phrases

		config_file = open("config.json", "rb")
		file_contents = json.loads(config_file.read().decode("utf-8"))
		admins = file_contents["admins"]
		control_phrases = file_contents["phrases"]

	except Exception as e:
		print("failed to read configuration file: {0}".format(str(e)))

def terminal():
	while True:
		command = input("> ")
		if command == "exit":
			break
		elif command == "reconfigure":
			configure()
		else:
			print("unrecognized command \"{0}\".".format(command))

if __name__ == "__main__":
	# perform initial configuration
	configure()

	email_server = smtplib.SMTP('smtp.gmail.com:587')
	email_server.ehlo()
	email_server.starttls()

	username = "batsignal.noreply@gmail.com"
	passwd = "batmailaccount"
	email_server.login(username, passwd)
    
	# spin up listener and work threads
	worker_threads.append(threading.Thread(target=threaded_listen))
	worker_threads.append(threading.Thread(target=threaded_parse))

	for thread in worker_threads:
		thread.start()

	try:
		# simple terminal emulator
		# warning: blocking function call
		terminal()
	except KeyboardInterrupt:
		pass

	join_threads_flag = True
	# join threads
	for thread in worker_threads:
		thread.join()
	# join queue
	message_queue.join()

	email_server.quit()

