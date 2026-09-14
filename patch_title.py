import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Title
    old_title = r"Metas &amp; Portfólio \(Araguaína\/TO\)|Metas & Portfólio \(Araguaína\/TO\)"
    new_title = "Metas & Portfólio Score 5"
    html = re.sub(old_title, new_title, html)

    # 2. Update Badge to Button
    old_badge = r'<span class="badge" style="background: rgba\(0, 255, 136, 0\.15\); color: var\(--primary-accent\); font-size: 0\.75rem; padding: 0\.25rem 0\.6rem; border-radius: 12px; font-weight: 600;">Aba Export • Tempo Real</span>'
    new_badge = """<button class="badge" onclick="this.innerText='⏳ Atualizando...'; carregarDadosDrive().then(() => this.innerText='🔄 Atualizar Dados');" style="background: rgba(0, 255, 136, 0.15); color: var(--primary-accent); font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 12px; font-weight: 600; cursor: pointer; border: 1px solid var(--primary-accent); transition: all 0.2s;">🔄 Atualizar Dados</button>"""
    html = re.sub(old_badge, new_badge, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
