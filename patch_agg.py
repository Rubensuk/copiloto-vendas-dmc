import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. ADD THE AGGREGATE METRICS HTML
    agg_html = """
                <!-- Métricas Agregadas (Barras de Progresso) -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-top: 1rem;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">📦 RGB (Vasilhames)</div>
                        <div id="agg-rgb-text" style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0/0 cxs</div>
                        <div id="agg-rgb-bar" style="margin-top: 5px;"></div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">🍺 600ml (Inteira + HE)</div>
                        <div id="agg-600-text" style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0/0 SKUs</div>
                        <div id="agg-600-bar" style="margin-top: 5px;"></div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">🍾 Long Neck</div>
                        <div id="agg-ln-text" style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0/0 cxs</div>
                        <div id="agg-ln-bar" style="margin-top: 5px;"></div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">🥃 300ml</div>
                        <div id="agg-300-text" style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0/0 cxs</div>
                        <div id="agg-300-bar" style="margin-top: 5px;"></div>
                    </div>
                </div>

                <!-- Lista Expandível de Clientes (Substitui Matriz de Gaps) -->"""
    
    html = html.replace('<!-- Lista Expandível de Clientes (Substitui Matriz de Gaps) -->', agg_html)

    # 2. UPDATE JS to calculate the aggregates and add the VISITA badge
    js_update = """
            // GERAR TABELA DE METAS E PORTFOLIO (ESTRUTURA STREAMLIT)
            const listContainer = document.getElementById('pdv-list-container');
            if (listContainer) {
                const HE_600 = {'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'BUD 600': 'Budweiser 600ml', 'COR 600': 'Corona 600ml', 'ORI 600': 'Original 600ml', 'OUTROS 600': 'Outros 600ml'};
                const HE_LN = {'COR LN': 'Corona Long Neck', 'STL LN': 'Stella Artois Long Neck', 'STL PG LN': 'Stella Puro Glúten Long Neck', 'SPT LN': 'Spaten Long Neck', 'MIC LN': 'Michelob Ultra Long Neck', 'OUTROS LN': 'Outros Long Neck', 'BUD LN': 'Budweiser Long Neck'};
                const CORE_600 = {'AP 600': 'Antarctica 600ml', 'BC 600': 'Brahma 600ml', 'BUD 600': 'Budweiser 600ml', 'ORI 600': 'Original 600ml', 'SK 600': 'Skol 600ml', 'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'OUTROS 600': 'Outros 600ml'};
                const CORE_300 = {'AP 300': 'Antarctica 300ml', 'BC 300': 'Brahma 300ml', 'BUD 300': 'Budweiser 300ml', 'ORI 300': 'Original 300ml', 'SK 300': 'Skol 300ml', 'OUTROS 300': 'Outros 300ml'};
                const CORE_1000 = {'AP 1000': 'Antarctica 1000ml', 'BC 1000': 'Brahma 1000ml', 'BUD 1000': 'Budweiser 1000ml', 'ORI 1000': 'Original 1000ml', 'SK 1000': 'Skol 1000ml', 'OUTROS 1000': 'Outros 1000ml'};
                
                function safeInt(val) {
                    if (!val || val.trim() === '') return 0;
                    const parsed = parseInt(parseFloat(val));
                    return isNaN(parsed) ? 0 : parsed;
                }
                function calcReal(row, mapping) {
                    let sum = 0;
                    for (const key in mapping) {
                        sum += safeInt(row[key]);
                    }
                    return sum;
                }
                function barraHTML(pct, label) {
                    let cor = pct < 40 ? '#ef4444' : (pct < 75 ? '#f59e0b' : '#22c55e');
                    let bg_bar = document.body.classList.contains('light-mode') ? '#e2e8f0' : '#2a2a3a';
                    return `
                    <div style="margin: 4px 0;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 2px;">
                            <span><b>${label}</b></span>
                            <span style="color: ${cor}; font-weight: 700;">${pct.toFixed(0)}%</span>
                        </div>
                        <div style="background: ${bg_bar}; border-radius: 6px; height: 18px; overflow: hidden;">
                            <div style="width: ${pct}%; height: 100%; background: ${cor}; border-radius: 6px; transition: width 0.3s;"></div>
                        </div>
                    </div>`;
                }
                function barraSmallHTML(pct) {
                    let cor = pct < 40 ? '#ef4444' : (pct < 75 ? '#f59e0b' : '#22c55e');
                    let bg_bar = document.body.classList.contains('light-mode') ? '#e2e8f0' : '#2a2a3a';
                    return `
                    <div style="background: ${bg_bar}; border-radius: 4px; height: 10px; overflow: hidden;">
                        <div style="width: ${pct}%; height: 100%; background: ${cor}; border-radius: 4px; transition: width 0.3s;"></div>
                    </div>
                    <div style="text-align: right; font-size: 0.65rem; color: ${cor}; font-weight: bold; margin-top: 2px;">${pct.toFixed(0)}%</div>`;
                }
                function gerarQuadrado(vendeu) {
                    return vendeu ? `<div style="width:16px;height:16px;background-color:#22c55e;border-radius:3px;margin:0 auto;"></div>` : `<div style="width:16px;height:16px;background-color:#ef4444;border-radius:3px;margin:0 auto;"></div>`;
                }

                let html_lista = `
                <div style="display:flex; padding:10px 15px; background:var(--table-header-bg, rgba(0,0,0,0.1)); font-weight:bold; font-size:0.9rem; border-bottom:2px solid var(--table-border, rgba(255,255,255,0.1)); margin-bottom:5px;">
                    <div style="flex: 2;">🏪 NOME DO PDV</div>
                    <div style="flex: 1;">📊 SEGMENTO</div>
                    <div style="flex: 1;">🎯 STATUS</div>
                    <div style="flex: 2; text-align:right;">📋 METAS</div>
                </div>`;
                
                let agg = {
                    meta_rgb: 0, real_rgb: 0,
                    meta_600: 0, real_600: 0,
                    meta_ln: 0, real_ln: 0,
                    meta_300: 0, real_300: 0
                };
                
                data.rows.forEach(row => {
                    let base = row['BASE'] ? row['BASE'].trim().toUpperCase() : 'CORE';
                    if (!base) base = 'CORE';
                    let bateu = parseFloat(row['BATEU META']) || 0;
                    let status_txt = bateu === 1 ? "<span style='color:#22c55e;'>✅ BATEU META</span>" : "<span style='color:#ef4444;'>❌ FORA DA META</span>";
                    let icone = base === 'CORE' ? "🟡" : (base === 'HIGH END' ? "💎" : "🏪");
                    
                    let meta_info = "";
                    let inner_html = "";
                    let is_light = document.body.classList.contains('light-mode');
                    let border_color = is_light ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.1)';
                    let row_bg = is_light ? 'rgba(0,0,0,0.02)' : 'rgba(255,255,255,0.03)';
                    let thead_bg = is_light ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)';
                    let text_color = is_light ? '#111827' : '#ffffff';
                    
                    let visita = row['VISITA'] || '';
                    let badge_visita = visita ? `<span style="background: rgba(100,116,139,0.2); padding: 2px 6px; border-radius: 4px; margin-left: 5px; font-size: 0.7rem; color: #94a3b8;">🗓️ ${visita}</span>` : '';

                    let meta_600 = safeInt(row['600']);
                    let real_600 = calcReal(row, HE_600);
                    let meta_ln = safeInt(row['LN']);
                    let real_ln = calcReal(row, HE_LN);
                    let meta_int = safeInt(row['INTEIRA']);
                    let real_int = calcReal(row, CORE_600);
                    let meta_rgb = safeInt(row['RGB']);
                    let meta_300 = safeInt(row['LITRINHO']);
                    let real_300 = calcReal(row, CORE_300);
                    let real_1000 = calcReal(row, CORE_1000);
                    let real_rgb = real_int + real_300 + real_1000;
                    
                    if (base === 'HIGH END') {
                        agg.meta_600 += meta_600; agg.real_600 += real_600;
                        agg.meta_ln += meta_ln; agg.real_ln += real_ln;
                        
                        meta_info = `600ml: ${meta_600} &nbsp;|&nbsp; Long Neck: ${meta_ln}`;
                        
                        let pct_600 = meta_600 > 0 ? (real_600 / meta_600 * 100) : 0;
                        let pct_ln = meta_ln > 0 ? (real_ln / meta_ln * 100) : 0;
                        
                        inner_html += barraHTML(pct_600, `🍺 600ml — Meta: ${meta_600} | Real: ${real_600} | Falta: ${Math.max(0, meta_600 - real_600)}`);
                        inner_html += barraHTML(pct_ln, `🍾 Long Neck — Meta: ${meta_ln} | Real: ${real_ln} | Falta: ${Math.max(0, meta_ln - real_ln)}`);
                        
                        let mix_items = "";
                        const formatRow = (sq, nome, val) => `<tr style="border-bottom:1px solid ${border_color};"><td style="padding:6px 12px;text-align:center;">${sq}</td><td style="padding:6px 12px;text-align:left;font-size:0.95rem;color:${text_color};">${nome}</td><td style="padding:6px 12px;text-align:center;font-weight:bold;color:${text_color};">${val}</td></tr>`;
                        
                        for (let col in HE_600) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_600[col], safeInt(row[col])); }
                        for (let col in HE_LN) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_LN[col], safeInt(row[col])); }
                        
                        inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (High End)</div>
                        <table style="width:100%; border-collapse:collapse; margin-top:5px; background:var(--table-header-bg, rgba(0,0,0,0.1)); border-radius:5px; overflow:hidden;">
                            <thead style="background:${thead_bg};font-size:0.9rem;">
                                <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                            </thead>
                            <tbody>${mix_items}</tbody>
                        </table>`;
                    } else if (base === 'CORE') {
                        agg.meta_600 += meta_int; agg.real_600 += real_int;
                        agg.meta_rgb += meta_rgb; agg.real_rgb += real_rgb;
                        agg.meta_300 += meta_300; agg.real_300 += real_300;
                        
                        meta_info = `Inteira: ${meta_int} &nbsp;|&nbsp; RGB: ${meta_rgb} &nbsp;|&nbsp; 300ml: ${meta_300}`;
                        
                        let pct_int = meta_int > 0 ? (real_int / meta_int * 100) : 0;
                        let pct_rgb = meta_rgb > 0 ? (real_rgb / meta_rgb * 100) : 0;
                        let pct_300 = meta_300 > 0 ? (real_300 / meta_300 * 100) : 0;
                        
                        inner_html += barraHTML(pct_int, `🍺 Inteira (600ml) — Meta: ${meta_int} | Real: ${real_int} | Falta: ${Math.max(0, meta_int - real_int)}`);
                        inner_html += barraHTML(pct_rgb, `📦 RGB (Vasilhames) — Meta: ${meta_rgb} | Real: ${real_rgb} | Falta: ${Math.max(0, meta_rgb - real_rgb)}`);
                        inner_html += barraHTML(pct_300, `🥃 300ml — Meta: ${meta_300} | Real: ${real_300} | Falta: ${Math.max(0, meta_300 - real_300)}`);
                        
                        let mix_items = "";
                        const formatRow = (sq, nome, val) => `<tr style="border-bottom:1px solid ${border_color};"><td style="padding:6px 12px;text-align:center;">${sq}</td><td style="padding:6px 12px;text-align:left;font-size:0.95rem;color:${text_color};">${nome}</td><td style="padding:6px 12px;text-align:center;font-weight:bold;color:${text_color};">${val}</td></tr>`;
                        
                        for (let col in CORE_600) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), CORE_600[col], safeInt(row[col])); }
                        for (let col in CORE_300) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), CORE_300[col], safeInt(row[col])); }
                        for (let col in CORE_1000) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), CORE_1000[col], safeInt(row[col])); }
                        
                        inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (Core)</div>
                        <table style="width:100%; border-collapse:collapse; margin-top:5px; background:var(--table-header-bg, rgba(0,0,0,0.1)); border-radius:5px; overflow:hidden;">
                            <thead style="background:${thead_bg};font-size:0.9rem;">
                                <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                            </thead>
                            <tbody>${mix_items}</tbody>
                        </table>`;
                    } else {
                        inner_html += `<div>Segmento Vitrine</div>`;
                    }
                    
                    html_lista += `
                    <details class="pdv-row pdv-item" data-nome="${row['NOME PDV']?.toLowerCase() || ''}" data-chave="${row['CHAVE PDV'] || ''}" style="background: ${row_bg}; border: 1px solid ${border_color}; border-radius: 8px; margin-bottom: 8px; font-family: sans-serif;">
                        <summary class="pdv-summary" style="padding: 12px 15px; cursor: pointer; display: flex; align-items: center; list-style: none;">
                            <div style="flex: 2; font-weight: bold; color: ${text_color};">${icone} ${row['NOME PDV'] || 'PDV'} <span style="font-size:0.75rem; color:#888; font-weight:normal; margin-left:5px;">${row['CHAVE PDV'] || ''}</span>${badge_visita}</div>
                            <div style="flex: 1; font-size: 0.9rem; color: ${text_color};">${base}</div>
                            <div style="flex: 1; font-size: 0.9rem; font-weight: bold;">${status_txt}</div>
                            <div style="flex: 2; text-align: right; font-size: 0.9rem; color: #888;">${meta_info}</div>
                        </summary>
                        <div class="pdv-details" style="padding: 15px; border-top: 1px solid ${border_color}; color: ${text_color};">
                            ${inner_html}
                        </div>
                    </details>`;
                });
                
                listContainer.innerHTML = html_lista;
                
                // Atualizar as barras agregadas
                let pct_agg_rgb = agg.meta_rgb > 0 ? (agg.real_rgb / agg.meta_rgb * 100) : 0;
                let pct_agg_600 = agg.meta_600 > 0 ? (agg.real_600 / agg.meta_600 * 100) : 0;
                let pct_agg_ln  = agg.meta_ln > 0 ? (agg.real_ln / agg.meta_ln * 100) : 0;
                let pct_agg_300 = agg.meta_300 > 0 ? (agg.real_300 / agg.meta_300 * 100) : 0;
                
                const elRgbText = document.getElementById('agg-rgb-text');
                const el600Text = document.getElementById('agg-600-text');
                const elLnText  = document.getElementById('agg-ln-text');
                const el300Text = document.getElementById('agg-300-text');
                
                if (elRgbText) elRgbText.innerText = `${agg.real_rgb}/${agg.meta_rgb} cxs`;
                if (el600Text) el600Text.innerText = `${agg.real_600}/${agg.meta_600} SKUs`;
                if (elLnText)  elLnText.innerText = `${agg.real_ln}/${agg.meta_ln} cxs`;
                if (el300Text) el300Text.innerText = `${agg.real_300}/${agg.meta_300} cxs`;
                
                const elRgbBar = document.getElementById('agg-rgb-bar');
                const el600Bar = document.getElementById('agg-600-bar');
                const elLnBar  = document.getElementById('agg-ln-bar');
                const el300Bar = document.getElementById('agg-300-bar');
                
                if (elRgbBar) elRgbBar.innerHTML = barraSmallHTML(pct_agg_rgb);
                if (el600Bar) el600Bar.innerHTML = barraSmallHTML(pct_agg_600);
                if (elLnBar)  elLnBar.innerHTML = barraSmallHTML(pct_agg_ln);
                if (el300Bar) el300Bar.innerHTML = barraSmallHTML(pct_agg_300);
            }
    """
    
    old_js_pattern = r"// GERAR TABELA DE METAS E PORTFOLIO \(ESTRUTURA STREAMLIT\).*?listContainer\.innerHTML = html_lista;\s*\}"
    html = re.sub(old_js_pattern, js_update.strip(), html, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
