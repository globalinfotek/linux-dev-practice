sudo systemctl disable apt-daily.service
sudo systemctl disable apt-daily.timer

sudo rm /var/lib/apt/lists/lock
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/updates/*

# Python
sudo alias python3="python3.8"
sudo apt install python3-pip -y

# Ansible
sudo apt-get install ansible -y
sudo python3.8 -m pip install ansible
