import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add Filter dropdown
    old_select_rn = r'(<select id="select-rn-code" onchange="atualizarPainelRN\(\)">.*?</select>\s*</div>)'
    new_select_rn = r'\1\n                    <div class="calc-input-group" style="margin-left: 10px;">\n                        <label for="select-dia-visita">Dia da Visita</label>\n                        <select id="select-dia-visita" onchange="atualizarPainelRN()">\n                            <option value="TODOS">Todos os Dias</option>\n                            <option value="SEG">Segunda-feira (SEG)</option>\n                            <option value="TER">Terça-feira (TER)</option>\n                            <option value="QUA">Quarta-feira (QUA)</option>\n                            <option value="QUI">Quinta-feira (QUI)</option>\n                            <option value="SEX">Sexta-feira (SEX)</option>\n                            <option value="SAB">Sábado (SAB)</option>\n                        </select>\n                    </div>'
    html = re.sub(old_select_rn, new_select_rn, html, flags=re.DOTALL)

    # 2. Add Filter & Sort logic in atualizarPainelRN
    old_foreach = r"data\.rows\.forEach\(row => \{"
    new_foreach = """
                const selectDia = document.getElementById('select-dia-visita');
                const diaFiltro = selectDia ? selectDia.value : "TODOS";
                
                let filteredRows = data.rows.filter(row => {
                    if (diaFiltro === "TODOS") return true;
                    let vis = row['VISITA'] || '';
                    return vis.toUpperCase().includes(diaFiltro);
                });
                
                filteredRows.sort((a, b) => {
                    let bateuA = safeInt(a['BATEU META']) === 1 ? 1 : 0;
                    let bateuB = safeInt(b['BATEU META']) === 1 ? 1 : 0;
                    return bateuA - bateuB;
                });
                
                filteredRows.forEach(row => {
                    agg.count_pdvs = (agg.count_pdvs || 0) + 1;
                    if (safeInt(row['BATEU META']) === 1) agg.count_bateu_meta = (agg.count_bateu_meta || 0) + 1;
"""
    html = re.sub(old_foreach, new_foreach, html)

    # 3. Update top metric boxes to use dynamic counts instead of data.meta/data.pdvs
    old_boxes = r"if \(score5PdvsEl\) score5PdvsEl\.innerText = `\$\{data\.meta\} de \$\{data\.pdvs\}`;.*?if \(metaBatidaEl\) metaBatidaEl\.innerText = `\$\{data\.meta\} PDVs`;"
    new_boxes = """if (score5PdvsEl) score5PdvsEl.innerText = `${agg.count_bateu_meta || 0} de ${agg.count_pdvs || 0}`;
                if (pdvsCoreEl) pdvsCoreEl.innerText = `${agg.count_core}`;
                if (pdvsHeEl) pdvsHeEl.innerText = `${agg.count_he}`;
                if (metaBatidaEl) metaBatidaEl.innerText = `${agg.count_bateu_meta || 0} PDVs`;"""
    html = re.sub(old_boxes, new_boxes, html, flags=re.DOTALL)

    # 4. Remove CHAVE PDV from the summary
    old_summary = r'<span style="font-size:0\.75rem; color:#888; font-weight:normal; margin-left:5px;">\$\{row\[\'CHAVE PDV\'\] \|\| \'\'\}</span>'
    html = re.sub(old_summary, "", html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
