#!/usr/bin/env bash

rm /var/lib/dpkg/lock
rm /var/cache/apt/archives/lock
rm /var/lib/apt/lists/lock
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install python3.9 -y
sudo apt-get install -y wine  
FILE=python-3.8.9.exe
if test -f "$FILE"; then
	echo "$FILE already exists."
else
	sudo wget https://www.python.org/ftp/python/3.8.9/python-3.8.9.exe
fi

sudo wine cmd /c python-3.8.9.exe /quiet InstallAllUsers=0
sudo wine "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/python.exe" -m pip install pyinstaller==4.6 cryptography==36.0.1
