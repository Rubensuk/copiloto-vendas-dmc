import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # REPLACE Matriz de Gaps with <div id="pdv-list-container">
    start_str = "<!-- Tabela / Matriz de Gaps (Real vs Falta) -->"
    end_str = "<!-- PapaParse para processar o CSV -->"
    
    start_idx = html.find(start_str)
    end_idx = html.find(end_str)
    if start_idx != -1 and end_idx != -1:
        new_content = '<!-- Lista Expandível de Clientes (Substitui Matriz de Gaps) -->\n                <div id="pdv-list-container" style="margin-top: 1rem;"></div>\n            </div>\n        </section>\n    </main>\n\n    <footer>\n        DMC Sales Copilot • Concepção e Desenvolvimento por <strong>Rubens Oliveira Silva</strong> © 2026.\n    </footer>\n\n    '
        html = html[:start_idx] + new_content + html[end_idx:]
    else:
        print("COULD NOT FIND MATRIZ DE GAPS")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
