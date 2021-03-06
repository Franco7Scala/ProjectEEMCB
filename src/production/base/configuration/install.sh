#!/usr/bin/env bash

# installing pip
sudo apt-get install python-pip

# installing required libraries
sudo pip install numpy
sudo pip install sklearn
sudo pip install MySQL-python
sudo pip install pysftp
sudo pip install holidays
sudo pip install requests
sudo pip install selenium
sudo pip install pathlib
sudo pip install pyvirtualdisplay

##############
sudo apt-get install python-pip python-dev libmysqlclient-dev
sudo apt-get install python-mysqldb



####### pyvirtualdisplay
sudo apt-get install python-pip
sudo apt-get install xvfb
sudo pip install pyvirtualdisplay

#sudo apt-get install xvfb xserver-xephyr vnc4server
# optional
sudo apt-get install python-pil scrot
sudo pip install pyscreenshot
# optional for examples
sudo pip install entrypoint2



# Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
