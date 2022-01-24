<h1 align="center">
  <br>
  <a href="https://github.com/3ct0s/"><img src="https://i.ibb.co/q0WRphJ/2019-01-22-5c4769cbb7755-lunar-eclipse-2019-199-skyandtelescope-removebg-preview.png" width=400 weigth=500 alt="Disctopia"></a>
  <br>
  Eclipse Grabber
  <br>
</h1>

<h4 align="center">Eclipse Discord Token Grabber</h4>

<p align="center">
    <img src="https://img.shields.io/badge/Supported_Platforms-Windows & OSX-red">
    <img src="https://img.shields.io/badge/Version-1.0-red">
    <img src="https://img.shields.io/badge/Python-3.8.9-red">
</p>

---

## What is Eclipse?

Eclipse is an open source Python Discord Token Grabber that can be used on Windows and OSX systems. With this tool you can generate exectubale files that will steal Discord tokens from a system and report them to your Discord server via Discord Webhooks.

## How does it work?

Like mentioned above, this tool is written in Python and can be used on Windows and OSX systems to exfiltrate Discord Tokens. Once executed it will look through the file system and attempt to locate a Discord Account Tokens. Once it finds one it will send a message to your Discord server via Discord Webhooks which will contain the token, information about the system and information about the Discord Account.
## How to Setup Eclipse?

> Please follow the [installation guide](inst/SETUP.md) to install the Eclipse Grabber.


## How to Build a Grabber?

> Please follow the [build guide](inst/BUILD.md) to build an executable grabber.

### Eclipse Grabber Features

- Gathers Infomartion about the system
- Send infomation about Discord Account
- Gathers Billing Information from account (if available)
- Encrypted Traffic (HTTPS)

## Malware Scan (Static Analysis)
We will occasionally scan the eclipse grabber on [antiscan.me](https://antiscan.me), here is our latest scan results:
![image](https://i.ibb.co/6Dms7mn/eclipse-scan-result.png)

## Contributors
For anyone who is interested in contributing to **Eclipse Grabber**, please make sure you fork the project and make a pull request.
## Disclaimer

This github repository is made for educational purposes only. The developers are not responsible for any misuse of this software. **Do not use this software for illegal purposes.**
