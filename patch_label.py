import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find and replace the label
    # Current: <label for="select-rn-code">Selecione o Roteiro (RN)</label>
    # Note: it might be uppercase in HTML or uppercase via CSS. The screen shows uppercase.
    # The source code had: <label for="select-rn-code">Selecione o Roteiro (RN)</label>

    html = html.replace('>Selecione o Roteiro (RN)<', '>SELECIONE O (RN)<')
    html = html.replace('>SELECIONE O ROTEIRO (RN)<', '>SELECIONE O (RN)<')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
