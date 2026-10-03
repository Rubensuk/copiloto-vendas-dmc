import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The block starts here:
    target_start = "<!-- Métricas Agregadas (Barras de Progresso) -->"
    target_end = "<!-- Lista Expandível de Clientes"
    
    # Use regex to remove everything from target_start up to target_end
    # Using re.DOTALL to match across newlines
    pattern = re.compile(re.escape(target_start) + r'.*?' + r'(?=' + re.escape(target_end) + r')', re.DOTALL)
    
    html = re.sub(pattern, "", html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
