import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace the HTML grid
    old_grid_pattern = r'<!-- 5 Métricas de Topo \(Score 5 Executivo\) -->\s*<div style="display: grid; grid-template-columns: repeat\(5, 1fr\); gap: 0\.6rem; margin-top: 1rem;">.*?</div>\s*<!-- Métricas Agregadas \(Barras de Progresso\) -->'
    
    new_grid_html = """<!-- 4 Métricas de Topo (Score 5 Executivo) -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-top: 1rem;">
                    <div style="background: rgba(0, 255, 136, 0.08); border: 1px solid rgba(0, 255, 136, 0.2); padding: 0.75rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.7rem; color: var(--primary-accent); font-weight: 600;">⭐ Score 5 (PDVs)</div>
                        <div id="rn-score5-pdvs" style="font-size: 1.2rem; font-weight: 700; color: #00ff88; margin-top: 0.1rem;">0 de 0</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary); font-weight: 600;">🟡 PDVs Core</div>
                        <div id="rn-pdvs-core" style="font-size: 1.2rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary); font-weight: 600;">💎 PDVs High End</div>
                        <div id="rn-pdvs-he" style="font-size: 1.2rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary); font-weight: 600;">✅ Bateram Meta (Geral)</div>
                        <div id="rn-meta-batida" style="font-size: 1.2rem; font-weight: 700; color: #00ff88; margin-top: 0.1rem;">0 PDVs</div>
                    </div>
                </div>

                <!-- Métricas Agregadas (Barras de Progresso) -->"""
    
    html = re.sub(old_grid_pattern, new_grid_html, html, flags=re.DOTALL)

    # 2. Update JS: Remove old element updates
    js_remove_pattern = r'const score5El = document\.getElementById\(\'rn-score-5\'\);.*?if \(foraEl\) foraEl\.innerText = `\$\{data\.pdvs - data\.meta\}`;'
    html = re.sub(js_remove_pattern, '', html, flags=re.DOTALL)

    # 3. Update JS: Add count_core and count_he to agg
    old_agg_init = r'let agg = \{\s*meta_rgb: 0, real_rgb: 0,\s*meta_600: 0, real_600: 0,\s*meta_ln: 0, real_ln: 0,\s*meta_300: 0, real_300: 0\s*\};'
    new_agg_init = """let agg = {
                    meta_rgb: 0, real_rgb: 0,
                    meta_600: 0, real_600: 0,
                    meta_ln: 0, real_ln: 0,
                    meta_300: 0, real_300: 0,
                    count_core: 0, count_he: 0
                };"""
    html = re.sub(old_agg_init, new_agg_init, html)

    # 4. Update JS: Count them inside data.rows.forEach
    old_base_check = r"if \(base === 'HIGH END'\) \{"
    new_base_check = """if (base === 'HIGH END') {
                        agg.count_he += 1;"""
    html = html.replace(old_base_check, new_base_check)

    old_base_check_2 = r"\} else if \(base === 'CORE'\) \{"
    new_base_check_2 = """} else if (base === 'CORE') {
                        agg.count_core += 1;"""
    html = html.replace(old_base_check_2, new_base_check_2)

    # 5. Update JS: Populate new elements at the end
    old_end_js = r"if \(el300Bar\) el300Bar\.innerHTML = barraSmallHTML\(pct_agg_300\);\s*\}"
    new_end_js = """if (el300Bar) el300Bar.innerHTML = barraSmallHTML(pct_agg_300);
                
                const score5PdvsEl = document.getElementById('rn-score5-pdvs');
                const pdvsCoreEl = document.getElementById('rn-pdvs-core');
                const pdvsHeEl = document.getElementById('rn-pdvs-he');
                const metaBatidaEl = document.getElementById('rn-meta-batida');
                
                if (score5PdvsEl) score5PdvsEl.innerText = `${data.meta} de ${data.pdvs}`;
                if (pdvsCoreEl) pdvsCoreEl.innerText = `${agg.count_core}`;
                if (pdvsHeEl) pdvsHeEl.innerText = `${agg.count_he}`;
                if (metaBatidaEl) metaBatidaEl.innerText = `${data.meta} PDVs`;
            }"""
    html = re.sub(old_end_js, new_end_js, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
