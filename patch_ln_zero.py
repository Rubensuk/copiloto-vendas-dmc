import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the dictionaries
    old_dicts = """const HE_LN = {'HE_COR LN': 'Corona LN', 'HE_STL LN': 'Stella Artois LN', 'HE_STL PG LN': 'Stella Puro Gold LN', 'HE_SPT LN': 'Spaten LN', 'HE_MIC LN': 'Michelob Ultra LN', 'HE_OUTROS LN': 'Outros LN', 'HE_BUD LN': 'Budweiser LN', 'HE_BUD LN ZERO': 'Budweiser Zero LN', 'HE_COR LN ZERO': 'Corona Zero LN', 'HE_OUTROS LN ZERO': 'Outros Zero LN'};"""
    new_dicts = """const HE_LN = {'HE_COR LN': 'Corona LN', 'HE_STL LN': 'Stella Artois LN', 'HE_STL PG LN': 'Stella Puro Gold LN', 'HE_SPT LN': 'Spaten LN', 'HE_MIC LN': 'Michelob Ultra LN', 'HE_BUD LN': 'Budweiser LN', 'HE_OUTROS LN': 'Outros LN'};
                const HE_LN_ZERO = {'HE_BUD LN ZERO': 'Budweiser Zero LN', 'HE_COR LN ZERO': 'Corona Zero LN', 'HE_OUTROS LN ZERO': 'Outros Zero LN'};"""
    html = html.replace(old_dicts, new_dicts)

    # 2. Add parsing variables
    old_vars = """                    let meta_ln = safeInt(row['LN']);
                    let real_ln = calcReal(row, HE_LN);
                    let meta_int = safeInt(row['INTEIRA']);"""
    new_vars = """                    let meta_ln = safeInt(row['LN']);
                    let real_ln = calcReal(row, HE_LN);
                    let meta_ln_zero = safeInt(row['LN ZERO']);
                    let real_ln_zero = calcReal(row, HE_LN_ZERO);
                    let meta_int = safeInt(row['INTEIRA']);"""
    html = html.replace(old_vars, new_vars)

    # 3. Update total logic
    old_totals = """                    let total_meta = base === 'HIGH END' ? (meta_600 + meta_ln) : (meta_int + meta_rgb + meta_300);
                    let total_real = base === 'HIGH END' ? (real_600 + real_ln) : (real_int + real_rgb + real_300);"""
    new_totals = """                    let total_meta = base === 'HIGH END' ? (meta_600 + meta_ln + meta_ln_zero) : (meta_int + meta_rgb + meta_300);
                    let total_real = base === 'HIGH END' ? (real_600 + real_ln + real_ln_zero) : (real_int + real_rgb + real_300);"""
    html = html.replace(old_totals, new_totals)

    # 4. Update HIGH END block (insight + pct + bars + mix)
    old_he_block = """                    if (base === 'HIGH END') {
                        agg.count_he += 1;
                        agg.meta_600 += meta_600; agg.real_600 += real_600;
                        agg.meta_ln += meta_ln; agg.real_ln += real_ln;
                        
                        meta_info = `600ml: ${meta_600} &nbsp;|&nbsp; Long Neck: ${meta_ln}`;
                        
                        let pct_600 = meta_600 > 0 ? (real_600 / meta_600 * 100) : 0;
                        let pct_ln = meta_ln > 0 ? (real_ln / meta_ln * 100) : 0;
                        
                        
                        let insight_he = "";
                        if (real_600 < meta_600) insight_he = "Falta vender " + (meta_600 - real_600) + " cx de 600ml.";
                        else if (real_ln < meta_ln) insight_he = "Falta vender " + (meta_ln - real_ln) + " cx de Long Neck.";
                        
                        if (insight_he !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_he}</div>` + inner_html;
                        }
                        inner_html += barraHTML(pct_600, `🍺 600ml — Meta: ${meta_600} | Real: ${real_600} | Falta: ${Math.max(0, meta_600 - real_600)}`);
                        inner_html += barraHTML(pct_ln, `🍾 Long Neck — Meta: ${meta_ln} | Real: ${real_ln} | Falta: ${Math.max(0, meta_ln - real_ln)}`);
                        
                        let mix_items = "";
                        const formatRow = (sq, nome, val) => `<tr style="border-bottom:1px solid ${border_color};"><td style="padding:6px 12px;text-align:center;">${sq}</td><td style="padding:6px 12px;text-align:left;font-size:0.95rem;color:${text_color};">${nome}</td><td style="padding:6px 12px;text-align:center;font-weight:bold;color:${text_color};">${val}</td></tr>`;
                        
                        for (let col in HE_600) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_600[col], safeInt(row[col])); }
                        for (let col in HE_LN) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_LN[col], safeInt(row[col])); }
                        
                        inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (High End)</div>"""

    new_he_block = """                    if (base === 'HIGH END') {
                        agg.count_he += 1;
                        agg.meta_600 += meta_600; agg.real_600 += real_600;
                        agg.meta_ln += meta_ln; agg.real_ln += real_ln;
                        
                        let tem_zero = meta_ln_zero > 0 || real_ln_zero > 0;
                        
                        meta_info = `600ml: ${meta_600} &nbsp;|&nbsp; LN: ${meta_ln}` + (tem_zero ? ` &nbsp;|&nbsp; LN Zero: ${meta_ln_zero}` : "");
                        
                        let pct_600 = meta_600 > 0 ? (real_600 / meta_600 * 100) : (real_600 > 0 ? 100 : 0);
                        let pct_ln = meta_ln > 0 ? (real_ln / meta_ln * 100) : (real_ln > 0 ? 100 : 0);
                        let pct_ln_zero = meta_ln_zero > 0 ? (real_ln_zero / meta_ln_zero * 100) : (real_ln_zero > 0 ? 100 : 0);
                        
                        
                        let insight_he = "";
                        if (real_600 < meta_600) insight_he = "Falta vender " + (meta_600 - real_600) + " cx de 600ml.";
                        else if (real_ln < meta_ln) insight_he = "Falta vender " + (meta_ln - real_ln) + " cx de Long Neck.";
                        else if (real_ln_zero < meta_ln_zero) insight_he = "Falta vender " + (meta_ln_zero - real_ln_zero) + " cx de Long Neck Zero.";
                        
                        if (insight_he !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_he}</div>` + inner_html;
                        }
                        inner_html += barraHTML(pct_600, `🍺 600ml — Meta: ${meta_600} | Real: ${real_600} | Falta: ${Math.max(0, meta_600 - real_600)}`);
                        inner_html += barraHTML(pct_ln, `🍾 Long Neck — Meta: ${meta_ln} | Real: ${real_ln} | Falta: ${Math.max(0, meta_ln - real_ln)}`);
                        if (tem_zero) {
                            inner_html += barraHTML(pct_ln_zero, `🧊 Long Neck Zero — Meta: ${meta_ln_zero} | Real: ${real_ln_zero} | Falta: ${Math.max(0, meta_ln_zero - real_ln_zero)}`);
                        }
                        
                        let mix_items = "";
                        const formatRow = (sq, nome, val) => `<tr style="border-bottom:1px solid ${border_color};"><td style="padding:6px 12px;text-align:center;">${sq}</td><td style="padding:6px 12px;text-align:left;font-size:0.95rem;color:${text_color};">${nome}</td><td style="padding:6px 12px;text-align:center;font-weight:bold;color:${text_color};">${val}</td></tr>`;
                        
                        for (let col in HE_600) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_600[col], safeInt(row[col])); }
                        for (let col in HE_LN) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_LN[col], safeInt(row[col])); }
                        for (let col in HE_LN_ZERO) { if (row[col] !== undefined && row[col] !== '') mix_items += formatRow(gerarQuadrado(safeInt(row[col]) > 0), HE_LN_ZERO[col], safeInt(row[col])); }
                        
                        inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (High End)</div>"""
    
    html = html.replace(old_he_block, new_he_block)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
