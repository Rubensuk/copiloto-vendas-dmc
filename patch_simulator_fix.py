import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the Python wrapper at the top
    if content.startswith('import os\n\nhtml_content = """'):
        content = content[len('import os\n\nhtml_content = """'):]

    # 2. Remove the Python wrapper at the bottom
    tail_str = '"""\n\nwith open(\'simulador.html\', \'w\', encoding=\'utf-8\') as f:\n    f.write(html_content)\n\nprint("simulator created successfully")'
    if content.endswith(tail_str):
        content = content[:-len(tail_str)]
    elif content.endswith(tail_str + '\n'):
        content = content[:-len(tail_str)-1]
    
    # Let's use regex to be safe about the tail
    content = re.sub(r'"""\n+with open\(\'simulador\.html\'.*?print\("simulator created successfully"\)\n*', '', content, flags=re.DOTALL)

    # 3. Change data.response to data.result
    content = content.replace('data.response || "Desculpe,', 'data.result || "Desculpe,')
    content = content.replace('let htmlReport = data.response', 'let htmlReport = data.result')

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

if __name__ == '__main__':
    patch()
