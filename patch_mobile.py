import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Injetar o bloco CSS Mobile-First Rigoroso
    css_mobile = """
    /* --- MOBILE-FIRST RIGOROSO --- */
    .pdv-summary {
        white-space: normal !important;
        word-break: break-word !important;
    }
    .grid-responsive-2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin-bottom: 12px;
    }
    .grid-responsive-3 {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
    }
    .trade-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 10px;
        border-radius: 12px;
    }
    .fat-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .fat-val-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .btn-gerar-sticky {
        position: sticky;
        bottom: 0;
        z-index: 10;
        margin-top: 24px;
        padding-bottom: 12px; /* respiro abaixo do botão */
        background: var(--bg-color); /* evita que fundo seja transparente */
    }

    @media (max-width: 639px) {
        .pdv-summary {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 8px !important;
        }
        .pdv-summary > div {
            text-align: left !important;
            width: 100% !important;
            flex: none !important;
        }
        .pdv-summary > div:first-child {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }
        
        .grid-responsive-2 { grid-template-columns: 1fr !important; }
        .grid-responsive-3 { grid-template-columns: 1fr !important; gap: 8px !important; }
        
        .trade-card {
            flex-direction: row !important;
            justify-content: space-between !important;
            align-items: center !important;
            text-align: left !important;
            padding: 8px 12px !important;
        }
        .trade-card > div:first-child { margin-bottom: 0 !important; }
        .trade-card > div:nth-child(2) { margin-bottom: 0 !important; flex: 1; margin-left: 8px; }
        
        .fat-card-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 6px !important;
        }
        .fat-val-row {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 4px !important;
        }
    }
    /* ----------------------------- */
    </style>
    """
    html = html.replace('</style>', css_mobile)

    # 2. Aplicar classes grid-responsive-2 nos cards HE e CORE
    html = html.replace('let cards_he = `<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 12px;">`;',
                        'let cards_he = `<div class="grid-responsive-2">`;')
    html = html.replace('let cards_core = `<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 12px;">`;',
                        'let cards_core = `<div class="grid-responsive-2">`;')
    
    # 3. Aplicar classes grid-responsive-3 na Execução
    html = html.replace('<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px;">',
                        '<div class="grid-responsive-3">')
    
    # 4. Inserir class="trade-card" nos 6 cards de execução (3 ativos, 3 inativos)
    html = html.replace('padding:10px; display:flex; flex-direction:column; justify-content:center; box-shadow:0 4px 10px',
                        'box-shadow:0 4px 10px').replace('padding:10px; display:flex; flex-direction:column; justify-content:center;', '')
    
    html = re.sub(
        r'(<div style="background:[^"]+; border:[^"]+; border-radius:12px;)',
        r'\1" class="trade-card',
        html
    )
    
    # 5. Aplicar classes no faturamento
    html = html.replace('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">',
                        '<div class="fat-card-header">')
    html = html.replace('<div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:6px;">Realizado:',
                        '<div class="fat-val-row" style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:6px;"><div>Realizado:')
    html = html.replace('</span> / Meta: R$ ${formatBRL(meta_task)}</div>',
                        '</span></div><div>Meta: R$ ${formatBRL(meta_task)}</div></div>')
    
    # 6. Atualizar botão para ficar sticky e espaçado
    target_btn = """let btn_copiloto = `<div style="margin-top: 24px; margin-bottom: 8px; text-align: center;">
                        <button onclick="chamarCopiloto(${index})" style="background: linear-gradient(90deg, #4f46e5, #6366f1, #8b5cf6); background-size: 200% auto; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: 900; font-size: 1.05rem; cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); text-shadow: 0 1px 3px rgba(0,0,0,0.3); transition: all 0.3s ease; animation: gradientPulse 3s ease infinite;">🤖 Gerar Tática no Copiloto</button>
                    </div>`;"""
                    
    replacement_btn = """let btn_copiloto = `<div class="btn-gerar-sticky" style="text-align: center; border-radius: 0 0 8px 8px;">
                        <button onclick="chamarCopiloto(${index})" style="background: linear-gradient(90deg, #4f46e5, #6366f1, #8b5cf6); background-size: 200% auto; color: white; border: none; padding: 14px 20px; border-radius: 12px; font-weight: 900; font-size: 1.05rem; cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); text-shadow: 0 1px 3px rgba(0,0,0,0.3); transition: transform 0.1s ease; animation: gradientPulse 3s ease infinite;" onmousedown="this.style.transform='scale(0.97)'" onmouseup="this.style.transform='scale(1)'" onmouseleave="this.style.transform='scale(1)'">🤖 Gerar Tática no Copiloto</button>
                    </div>`;"""
    html = html.replace(target_btn, replacement_btn)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    # Bump SW cache
    with open('sw.js', 'r', encoding='utf-8') as f:
        sw = f.read()
    sw = re.sub(r"const CACHE_NAME = 'dmc-copilot-v\d+';", "const CACHE_NAME = 'dmc-copilot-v12';", sw)
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(sw)

if __name__ == '__main__':
    patch()
