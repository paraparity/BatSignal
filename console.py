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
#Requirements:
#Change json config files
#Change hostnames
app = Flask(__name__)

POOL_TIME = 5
messages = []
dataLock = threading.Lock()
threadHandler = threading.Thread()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = updateConfig(request.form)
    onlineList = []
    ips = getIpAddresses()
    onlineList = isServerAvailable(ips)
    hs = getHostNames(ips)

    if request.method == 'POST' and request.form['category'] == "ip":
        ip = str(request.form['data'])
        print("Restarting "+ip)
        restartNode(ip)

    elif request.method == 'POST' and request.form['category'] == "hostname":
        hostname = str(request.form['data'])
        ipAddress = str(request.form['ip'])
        changeHostName(hostname,ipAddress)
        print("Changing hostname")


    return render_template("index.html",form = form, iptable=zip(hs, ips, onlineList), messages=messages)


@app.route('/config', methods=['GET', 'POST'])
def serveConfig():
    form = updateConfig(request.form)
    f = open("config.json", "r+")
    data = json.load(f)
    removedAdmin = False
    #if request.method == 'POST' and request.form['admin'] is not None:
      #  data['admins'].remove(str(request.form['admin']))

    if request.method == 'POST':
        try:
            dataToRemove = request.form['data']
            category = request.form['category']
            data[category].remove(dataToRemove)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
            removedAdmin = True
            return redirect(url_for("serveConfig"))
        except KeyError:    
            if form.validate() and removedAdmin is False:
                print(str(form.phrases.data) == "None")
                if form.admins.data is not None:
                    data['admins'].append(form.admins.data)
                if !(str(form.phrases.data) == "None"): 
                    data['phrases'].append(form.phrases.data)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.close()
                return redirect(url_for("serveConfig"))

    return render_template('config.html', form=form, admins=data['admins'], phrases=data['phrases'])


def restartNode(ipAddress):
    command = "ssh pi@"+ipAddress+" echo raspberry | sudo -S /sbin/reboot"
    os.system(command)

def getHostNames(ips):
    hostnames = []
    for ip in ips:
        try:
            hostnames.append(socket.gethostbyaddr(ip)[0])
        except socket.gaierror:
            hostnames.append("None")
    return hostnames


def changeHostName(hostname, ipAddress):
    #command = "ssh pi@"+ipAddress+" echo raspberry | sudo -S sed -i 's/ubuntu/new-hostname/g' /etc/hosts'"
    command = "ssh pi@"+ipAddress+" echo raspberry | sudo -S hostname "+hostname
    os.system(command)
    print(command)


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


#Background Threads to query the message file
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
    messages.reverse()
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
    app.secret_key = 'super secret key'
    app.run(debug=True, port=5050)