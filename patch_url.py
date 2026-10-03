import re

def patch():
    with open('api/sheet.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # Old URL: https://docs.google.com/spreadsheets/d/1I7mM2zzqLABFnxi2Lx_-Sk86HrvmCRvv/export?format=csv&gid=1015537580
    # New URL: https://docs.google.com/spreadsheets/d/1IHbnIjofO3ozVBrywfb4bzGUsktE3Fu0/export?format=csv&gid=378465162
    
    old_url = 'https://docs.google.com/spreadsheets/d/1I7mM2zzqLABFnxi2Lx_-Sk86HrvmCRvv/export?format=csv&gid=1015537580'
    new_url = 'https://docs.google.com/spreadsheets/d/1IHbnIjofO3ozVBrywfb4bzGUsktE3Fu0/export?format=csv&gid=378465162'
    
    code = code.replace(old_url, new_url)

    with open('api/sheet.js', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    patch()
