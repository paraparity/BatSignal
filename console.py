from flask import Flask, render_template, request, flash, url_for, redirect
import threading
import atexit
import json
import socket
import subprocess
import re
import os
import time
from forms import updateConfig

#TODO
#Remote Restart
#Remote Hostname configuration
app = Flask(__name__)

POOL_TIME = 5
messages = []
dataLock = threading.Lock()
threadHandler = threading.Thread()
updatePage = True
lastTime = time.time()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    onlineList = []
    ips = getIpAddresses()
    onlineList = isServerAvailable(ips)
    hs = getHostNames(ips)
    global updatePage

    if updatePage == True and request.method == 'POST' and (time.time()-lastTime >5):
        return True

    return render_template("index.html", iptable=zip(hs, ips, onlineList), messages=messages)


@app.route('/config', methods=['GET', 'POST'])
def serveConfig():
    form = updateConfig(request.form)
    f = open("config.json", "r+")
    data = json.load(f)

    updated = False
    if request.method == 'POST' and form.validate():
        data['admins'].append(form.admins.data)
        data['phrases'].append(form.phrases.data)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.close()
        return redirect(url_for("index"))
    return render_template('config.html', form=form, update=updated, admins=data['admins'], phrases=data['phrases'])


def restartNode(ipAddress):
    print("Restarted!")


def getHostNames(ips):
    hostnames = []
    for ip in ips:
        try:
            hostnames.append(socket.gethostbyaddr(ip)[0])
        except socket.gaierror:
            hostnames.append("None")
    return hostnames


def changeHostName(hostname):
    print("Changed!")
    command = "ssh pi@192.168.1.XXX 'sudo sed -i 's/ubuntu/new-hostname/g' /etc/hosts'"


def getIpAddresses():
    command = "arp -a"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(output))
    return ips


def isServerAvailable(ipAddresses):
    onlineList = []
    for i in ipAddresses:
        command = "ping -c 1 -t 5 "+i+" >/dev/null 2>&1"
        response = os.system(command)

        if response == 0:
            onlineList.append(True)
        else:
            onlineList.append(False)
    return onlineList


def interrupt():
    global threadHandler
    threadHandler.cancel()


def getNewAlerts():
    global messages
    global threadHandler
    messages.clear()
    tempMessage = open('static/messages','r+')
    with dataLock:
        for line in tempMessage:
            messages.append(line)
    tempMessage.close()
    time.sleep(60)
    threadHandler = threading.Timer(POOL_TIME,getNewAlerts,())
    threadHandler.start()


def getNewAlertsStart():
    global threadHandler

    threadHandler = threading.Timer(POOL_TIME, getNewAlerts,())
    threadHandler.start()
if __name__ == '__main__':
    getNewAlertsStart()
    atexit.register(interrupt)
    app.secret_key = 'DOES_NOT_MATTER'
    app.run(debug=True, port=5050)