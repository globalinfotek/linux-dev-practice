# linux-dev-practice
Practice exercises for a senior Linux developer.

## Description

This repo contains a set of practice exercises dedicated to Linux system programming: user, kernel.  It also contains a Vagrant/Ansible-provisioned Common Development Environment (CDE) to facilitate the development, research, use, and testing of the practice exercises.  Follow the Usage steps below to get started.

## Usage

### Start Here

- [Install Virtualbox 6](https://www.virtualbox.org/wiki/Downloads)
- [Install Vagrant](https://www.vagrantup.com/downloads)
- `git clone https://github.com/globalinfotek/linux-dev-practice.git`
- `cd linux-dev-practice`
- `vagrant up`  (and be patient)
- `vagrant reload`  (allows the desktop environment to start)
- Log in with password `vagrant`

**NOTE:** You may need to increase the default Virtualbox settings for this machine (see: Machine --> Settings)
- Shared Clipboard: General --> Advanced
- Base Memory: System --> Motherboard
- Number of Processors: System --> Processor (min: 2)

**NOTE2:**
If running vagrant inside of a VM(i.e Windows host >  Linux running vagrant) ensure you change the processor settings for that vm to enable the setting `Virtualize Intel VT-x/EPT or AMD-V/RVI`. 

### Start of Day

`vagrant up`

-or-

`vagrant up --provision` (to ensure your CDE is up to date)

### Practice Exercises

TO DO: DON'T DO NOW... Write this in LIDE-004

### Done

#### End of Day

`vagrant halt`

#### Gone Forever

`vagrant destroy` (use with caution)

## POCs

Program Manager:

	Scott Krueger
	skrueger@us.globalinfotek.com

Project Lead:

	Joseph "Hark" Harkleroad
	jharkleroad@us.globalinfotek.com
