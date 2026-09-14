import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject the Quick Filter buttons in the HTML
    quick_filters_html = """
                    <div class="calc-input-group">
                        <label for="busca-pdv-input">🔍 Filtrar por Nome do PDV ou Chave</label>
                        <input type="text" id="busca-pdv-input" placeholder="Ex: Bar do Zé ou 10492" oninput="filtrarPDVsPainel()">
                        <div style="display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap;" id="quick-filters">
                            <button onclick="window.filtroStatus='FALTA_META'; filtrarPDVsPainel();" style="background: rgba(255,82,82,0.15); color: #ff5252; border: 1px solid #ff5252; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; cursor: pointer;">🔴 Falta Bater Meta</button>
                            <button onclick="window.filtroStatus='BATEU_META'; filtrarPDVsPainel();" style="background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid #00ff88; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; cursor: pointer;">🟢 Meta Batida</button>
                            <button onclick="window.filtroStatus='TODOS'; filtrarPDVsPainel();" style="background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; cursor: pointer;">Mostrar Todos</button>
                        </div>
                    </div>"""
    
    html = re.sub(r'<div class="calc-input-group">\s*<label for="busca-pdv-input">🔍 Filtrar por Nome do PDV ou Chave</label>\s*<input type="text" id="busca-pdv-input" placeholder="Ex: Bar do Zé ou 10492" oninput="filtrarPDVsPainel\(\)">\s*</div>', quick_filters_html, html)

    # 2. Rewrite filtrarPDVsPainel() to actually filter the DOM!
    new_js = """
        window.filtroStatus = 'TODOS';
        function filtrarPDVsPainel() {
            const query = (document.getElementById('busca-pdv-input')?.value || '').trim().toLowerCase();
            const items = document.querySelectorAll('.pdv-item');
            let visiveis = 0;
            
            items.forEach(item => {
                const nome = (item.getAttribute('data-nome') || '').toLowerCase();
                const chave = (item.getAttribute('data-chave') || '').toLowerCase();
                const bateu = item.getAttribute('data-bateu') === '1';
                
                let textMatch = nome.includes(query) || chave.includes(query);
                let statusMatch = true;
                
                if (window.filtroStatus === 'FALTA_META') statusMatch = !bateu;
                if (window.filtroStatus === 'BATEU_META') statusMatch = bateu;
                
                if (textMatch && statusMatch) {
                    item.style.display = 'block';
                    visiveis++;
                } else {
                    item.style.display = 'none';
                }
            });
            
            const badge = document.getElementById('pdv-filtrado-badge');
            if (badge) {
                badge.innerText = `Mostrando ${visiveis} PDVs`;
            }
            
            // Highlight the active quick filter button
            const btns = document.querySelectorAll('#quick-filters button');
            if(btns.length > 0) {
                btns[0].style.opacity = (window.filtroStatus === 'FALTA_META' || window.filtroStatus === 'TODOS') ? '1' : '0.5';
                btns[1].style.opacity = (window.filtroStatus === 'BATEU_META' || window.filtroStatus === 'TODOS') ? '1' : '0.5';
                btns[2].style.opacity = (window.filtroStatus === 'TODOS') ? '1' : '0.5';
            }
        }
"""
    html = re.sub(r'function filtrarPDVsPainel\(\) \{.*?(?=\n\s*// Inicializa dados carregando do Drive)', new_js, html, flags=re.DOTALL)

    # 3. Add data-bateu attribute and Opportunity Insight to html_lista generation
    # We need to find the string `html_lista += \n<details class="pdv-row pdv-item"` and modify it.
    
    # Let's do this by string replace where the html_lista string is built
    html = html.replace('data-chave="${row[\'CHAVE PDV\'] || \'\'}" style=', 'data-chave="${row[\'CHAVE PDV\'] || \'\'}" data-bateu="${bateu}" style=')

    # To inject the Insight badge, we can find where `inner_html` starts and replace it with dynamic logic inside `atualizarPainelRN()`
    # Actually, we can inject it where `inner_html += barraHTML(` starts in the CORE logic.
    insight_logic = """
                        let insight = "";
                        if (real_int < meta_int) insight = "Falta vender " + (meta_int - real_int) + " cx de 600ml.";
                        else if (real_rgb < meta_rgb) insight = "Falta vender " + (meta_rgb - real_rgb) + " cx de Vasilhame (RGB).";
                        else if (real_300 < meta_300) insight = "Falta vender " + (meta_300 - real_300) + " cx de 300ml.";
                        
                        if (insight !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight}</div>` + inner_html;
                        }
                        inner_html += barraHTML"""
    
    html = html.replace("inner_html += barraHTML", insight_logic, 1)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
