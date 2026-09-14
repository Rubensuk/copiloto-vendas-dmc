import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The block looks like:
    # let endpoint = "/api/generate";
    # if (window.location.protocol === 'file:') {
    #     // Se estiver rodando como arquivo local (duplo clique), aponta para a API implantada na Vercel
    #     endpoint = "https://copiloto-vendas-omega.vercel.app/api/generate";
    # }

    old_block = r"let endpoint = \"/api/generate\";\s*if\s*\(window\.location\.protocol\s*===\s*'file:'\)\s*\{\s*//.*?\s*endpoint = \"https://copiloto-vendas-omega\.vercel\.app/api/generate\";\s*\}"
    new_block = 'const endpoint = "https://copiloto-vendas-omega.vercel.app/api/generate";'
    
    html = re.sub(old_block, new_block, html, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
