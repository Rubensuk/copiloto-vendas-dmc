import urllib.request
import re

html = urllib.request.urlopen('https://dmc-copilot.vercel.app').read().decode('utf-8')
match = re.search(r'(<select id="select-rn-code"[^>]*>.*?</select>)', html, re.DOTALL)
if match:
    print(match.group(1))
else:
    print("Not found")
