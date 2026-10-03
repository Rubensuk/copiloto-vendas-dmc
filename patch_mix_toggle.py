import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # PATCH HIGH END
    target_he = """inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (High End)</div>
                        <table style="width:100%; border-collapse:collapse; margin-top:5px; background:var(--table-header-bg, rgba(0,0,0,0.1)); border-radius:5px; overflow:hidden;">
                            <thead style="background:${thead_bg};font-size:0.9rem;">
                                <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                            </thead>
                            <tbody>${mix_items}</tbody>
                        </table>`;"""
                        
    replacement_he = """inner_html += `
                        <details style="margin-top:15px; background: rgba(255,255,255,0.02); border-radius: 6px; border: 1px solid ${border_color};">
                            <summary style="padding: 10px; font-weight: bold; cursor: pointer; outline: none;">📦 Exibir Mix de Produtos (High End)</summary>
                            <table style="width:100%; border-collapse:collapse; border-top: 1px solid ${border_color}; background:var(--table-header-bg, transparent);">
                                <thead style="background:${thead_bg};font-size:0.9rem;">
                                    <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                                </thead>
                                <tbody>${mix_items}</tbody>
                            </table>
                        </details>`;"""
    
    html = html.replace(target_he, replacement_he)

    # PATCH CORE
    target_core = """inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (Core)</div>
                        <table style="width:100%; border-collapse:collapse; margin-top:5px; background:var(--table-header-bg, rgba(0,0,0,0.1)); border-radius:5px; overflow:hidden;">
                            <thead style="background:${thead_bg};font-size:0.9rem;">
                                <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                            </thead>
                            <tbody>${mix_items}</tbody>
                        </table>`;"""
                        
    replacement_core = """inner_html += `
                        <details style="margin-top:15px; background: rgba(255,255,255,0.02); border-radius: 6px; border: 1px solid ${border_color};">
                            <summary style="padding: 10px; font-weight: bold; cursor: pointer; outline: none;">📦 Exibir Mix de Produtos (Core)</summary>
                            <table style="width:100%; border-collapse:collapse; border-top: 1px solid ${border_color}; background:var(--table-header-bg, transparent);">
                                <thead style="background:${thead_bg};font-size:0.9rem;">
                                    <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                                </thead>
                                <tbody>${mix_items}</tbody>
                            </table>
                        </details>`;"""

    html = html.replace(target_core, replacement_core)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
