import time
import subprocess
import sys
import os
import requests

# config
bot_data = 'bot_id:api_token'
chat_id = 'chat_id'
hostname = subprocess.Popen('hostname', stdout=subprocess.PIPE, shell=True).communicate()[0]


# get last meaningful line from auth.log file
def check():
    cmd = "cat {path} | grep \"session opened\" | grep -v CRON | tail -1".format(path=path)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (line, err) = proc.communicate()
    return line


# send a message to configured Telegram broadcast channel
def notify(content):
    url = "https://api.telegram.org/bot{bot_data}/sendMessage?text={msg}&chat_id" \
          "={chat_id} "
    url = url.format(bot_data=bot_data, msg=content, chat_id=chat_id)
    requests.request("GET", url.encode('utf-8').strip(), headers={}, data={})
    return


if len(sys.argv) != 2:                          # check if arguments provided
    print("usage: python reporter.sh <path/to/auth.log>")
    exit(1)

path = sys.argv[1]                              # read auth.log path from run argument
if not os.access(path, os.R_OK):                # check if file can be read
    print('lacking read permissions or file is missing: {path}'.format(path=path))
    exit(2)
print('path: {path}'.format(path=path))

last_line = check()
notify('sudo monitor started ({host})'.format(host=hostname))

while True:
    current_line = check()
    if last_line != current_line:
        last_line = current_line
        msg = 'new sudo session opened ({host})'.format(host=hostname)
        notify(msg)
    time.sleep(1)
