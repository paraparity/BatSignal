cd setup/sensor

# Configure network interfaces
cp interfaces /etc/network/interfaces

# Configure bat-signal-node
cp bat-signal-node /etc/init.d/bat-signal-node
update-rc.d bat-signal-node defaults

# install required dependencies for sensor node module

# install portaudio v19+
apt-get install libasound-dev wget < "Y"
wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
tar -xvf pa_stable_v19_20140130.tgz
cd portaudio
./configure
make
make install
cd ..

# install pyaudio
git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
cd pyaudio
python3 setup.py install

# install pulseaudio & flac
aptitude install pulseaudio flac < "Y"

# configure kernel for sound drivers
cp alsa-base.conf /etc/modprobe.d/alsa-base.conf
cp modules /etc/modules

# clean up
rm -rf portaudio
rm -rf pyaudio

cd ../..
