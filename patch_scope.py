import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Define prepararCopiloto globally
    target = """        function prepararCopiloto(dataStr) {"""
    replacement = """        window.prepararCopiloto = function(dataStr) {"""
    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
