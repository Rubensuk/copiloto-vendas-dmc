import re

def patch():
    with open('api/sheet.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # The old ID
    old_url = 'https://docs.google.com/spreadsheets/d/1RdtvJaS0S1jeSNgBoYZ86WzIfvEIKlo8/export?format=csv'
    # The new ID provided by the user today
    new_url = 'https://docs.google.com/spreadsheets/d/1I7mM2zzqLABFnxi2Lx_-Sk86HrvmCRvv/export?format=csv&gid=1015537580'
    
    code = code.replace(old_url, new_url)

    with open('api/sheet.js', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    patch()
