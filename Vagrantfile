# All Vagrant configuration is done below. The "2" in vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unles you know what
# you're doing.
Vagrant.configure("2") do |config|
# The most common configuration options are documented and commented below.
# For a complete reference, please see the online documentation at
# https://docs.vagrantup.com
  config.ssh.username = "vagrant"
  config.ssh.insert_key = false
  config.vbguest.auto_update = true
  # config.vm.define "development" do |dev|
  config.vm.hostname = "LDP-CDE-v0.0.1"
  config.vm.box = "ubuntu/focal64"
  config.vm.box_version = "20200430.1.0"
  config.vm.synced_folder ".", "/home/vagrant/linux-dev-practice"
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true
    vb.customize ["modifyvm", :id, "--vram", "128"]
    vb.customize ["modifyvm", :id, "--vrde", "off"]
  end
  # Update repositories
  config.vm.provision :shell, inline: "sudo apt update -y"

  # Upgrade installed packages
  config.vm.provision :shell, inline: "sudo apt upgrade -y"

  # Add desktop environment
  config.vm.provision :shell, inline: "sudo apt install -y --no-install-recommends ubuntu-desktop"
  config.vm.provision :shell, inline: "sudo apt install -y --no-install-recommends virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11"
  # Add `vagrant` to Administrator
  config.vm.provision :shell, inline: "sudo usermod -a -G sudo vagrant"
  # Shell script
  config.vm.provision "shell",
    path: "./devops/vagrant/provision.sh"
end
