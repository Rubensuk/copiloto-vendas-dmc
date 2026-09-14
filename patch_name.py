import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('Stella Puro Glúten', 'Stella Puro Gold')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
