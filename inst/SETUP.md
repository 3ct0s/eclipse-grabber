# Setup Guide for {Token grabber}
Please follow the following steps to setup Disctopia.

 ## Step 1# Create the Server

You need to create a Discord server. 

Click on plus icon on discord left bar, give your server a name and click on the "Create" button.

![image](https://imgur.com/8q2rcHt.png)

## Step 2# Create text channel

You need to create a Tokens channel. 

Click on your server left bar with right mouse button, click on "Create Channel", name it "tokens" and click on "Create Channel".

![image](https://imgur.com/LoNrnt2.png)

## Step 3# Create the Webhook

You need to create Discord Webhook from your **Servers Settings >> Intergrations >> Webhooks.**

- Name it "Token" and set it's channel to **"tokens"**

![image](https://i.ibb.co/wccPgCx/Capture.png)

## Step 4# Install {Token grabber}

You need to clone the repository, cd into the cloned project files, run a command to change the permissions of the setup file and run it.
```
git clone https://github.com/3ct0s/discord-token-grabber.git
cd discord-token-grabber
```
### Windows
```
powershell.exe -ExecutionPolicy Bypass -Command .\setup_files\setup-win.ps1
```
### MacOS
```
chmod +x ./setup_files/setup-mac.sh
sudo ./setup_files/setup-mac.sh
```
### Linux
```
chmod +x ./setup_files/setup-lin.sh
sudo ./setup_files/setup-lin.sh
```
You might will be asked to say **yes** or **no** while installing the needed dependencies. Make sure you select **yes** and press enter.

![image](https://i.ibb.co/GVHVYdZ/Capture.png)


You will also be asked to install **Python 3.8.9**, please click on **"Install Now"** and **"Close"** when the installation is done

![image](https://i.ibb.co/f82KVNS/Capture.png)

Once you are done with the installation you can move to the next step which is building.

## Build {Token grabber}

Follow the [build guide](BUILD.md) to setup {Token grabber}.
