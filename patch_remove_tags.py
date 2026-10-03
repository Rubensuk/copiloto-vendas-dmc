import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target = """                        <div style="font-weight: bold; margin-bottom: 10px;">🎯 Faturamento & BEES Force</div>
                        <div style="display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
                            ${comprador === 1 ? '<span style="background:rgba(34,197,94,0.2); color:#22c55e; border:1px solid #22c55e; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">✅ Comprador no Mês</span>' : '<span style="background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid #ef4444; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🚨 Não Comprador (NC)</span>'}
                            ${cerv_tend ? `<span style="background:rgba(255,255,255,0.05); border:1px solid ${border_color}; padding:4px 8px; border-radius:4px; font-size:0.8rem;">🍺 Cerveja: ${cerv_tend} vs LY</span>` : ''}
                            ${he_tend ? `<span style="background:rgba(255,255,255,0.05); border:1px solid ${border_color}; padding:4px 8px; border-radius:4px; font-size:0.8rem;">💎 High End: ${he_tend} vs LY</span>` : ''}
                        </div>`;"""

    replacement = """                        <div style="font-weight: bold; margin-bottom: 10px;">🎯 Faturamento & BEES Force</div>`;"""

    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
