import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add button to header
    old_btn = r'<button id="btn-theme-toggle"'
    new_btn = r'<a href="simulador.html" class="btn-limpar-campos" style="text-decoration: none; margin-right: 10px; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border: 1px solid #3b82f6;" title="Ir para o Simulador de Vendas">🎮 Modo Treinamento</a>\n        <button id="btn-theme-toggle"'
    
    html = re.sub(old_btn, new_btn, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
