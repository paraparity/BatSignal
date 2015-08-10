cd setup/control

# install dhcp
apt-get install isc-dhcp-server < "Y"
cp dhcp.conf /etc/dhcp/dhcp.conf

# configure network interfaces
cp interface /etc/network/intefaces

# configure ip tables
./iptables.sh
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# configure bat signal gateway
cp bat-signal-gateway /etc/init.d/bat-signal-gateway
update-rc.d bat-signal-gateway defaults

# install dependencies for control node module
apt-get install python3 pyhton3-dev < "Y"

# install python 3.4
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar -xvf Python-3.4.3.tgz
cd Python-3.4.3
./configure
make
make install

wget https://bootstrap.pypa.io/get-pip.py
python3.4 get-pip.py

pip-3.4 install flask

cd ../..

rm -rf Python-3.4.3

