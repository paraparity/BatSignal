cd setup/sensor

# Configure network interfaces
cp interfaces /etc/network/interfaces

# Configure bat-signal-node
cp bat-signal-node /etc/init.d/bat-signal-node
update-rc.d bat-signal-node defaults

cd ../..
