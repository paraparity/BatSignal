# Setting up the Sensor node

It is important to note that the following instructions assume that you have install the `git` and `wget` packages.  If you have not you can just use `sudo apt-get install` to install them.

#### Install Python3

The sensor modules require python3+ to run.  To install python 3 use the following command `sudo apt-get install python3 python3-dev`.  It is important to note that after installing python 3 the file /usr/bin/python will still point to /usr/bin/python2.  This means that in order to run the modules you need to run it using python3 or modify /usr/bin/python to point to /usr/bin/python3.

#### Install PortAudio v19+

```
sudo apt-get install libasound-dev

wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
tar -xvf pa_stable_v19_20140130.tgz
cd pa_stable_v19_20140130

./configure
make
sudo make install
```

#### Install PyAudio

```
git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
cd pyaudio

python3 setup.py install
```

## Configuration

There are two files that need to be modified.

/etc/modprobe.d/alsa-base.conf (unmodified)
```
# autoloader aliases
install sound-slot-0 /sbin/modprobe snd-card-0
install sound-slot-1 /sbin/modprobe snd-card-1
install sound-slot-2 /sbin/modprobe snd-card-2
install sound-slot-3 /sbin/modprobe snd-card-3
install sound-slot-4 /sbin/modprobe snd-card-4
install sound-slot-5 /sbin/modprobe snd-card-5
install sound-slot-6 /sbin/modprobe snd-card-6
install sound-slot-7 /sbin/modprobe snd-card-7
# Cause optional modules to be loaded above generic modules
install snd /sbin/modprobe --ignore-install snd && { /sbin/modprobe --quiet snd-ioctl32 ; /sbin/modprobe --quiet snd-seq ; : ; }
install snd-rawmidi /sbin/modprobe --ignore-install snd-rawmidi && { /sbin/modprobe --quiet snd-seq-midi ; : ; }
install snd-emu10k1 /sbin/modprobe --ignore-install snd-emu10k1 && { /sbin/modprobe --quiet snd-emu10k1-synth ; : ; }
# Keep snd-pcsp from beeing loaded as first soundcard
options snd-pcsp index=-2
# Keep snd-usb-audio from beeing loaded as first soundcard
options snd-usb-audio index=-2
# Prevent abnormal drivers from grabbing index 0
options bt87x index=-2
options cx88_alsa index=-2
options snd-atiixp-modem index=-2
options snd-intel8x0m index=-2
options snd-via82xx-modem index=-2
```

Change this line `options snd-usb-audio index=-2` to `index=0`.
Add the line `options snd-bcm2835 index=-2`.

/etc/modules (unmodified)
```
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.
# Parameters can be specified after the module name.

snd-bcm2835
```

Add the line `snd-usb-audio`.

## Packages

Run the following command to install necessary packages `sudo aptitude install pulseaudio flac`.

