import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject the robust window.chamarCopiloto function right after <script>
    target_script = "<script>"
    chamar_copiloto_fn = """<script>
        window.chamarCopiloto = function(index) {
            try {
                if (!window.appFilteredRows || !window.appFilteredRows[index]) {
                    alert("Erro: Dados do PDV não encontrados na memória.");
                    return;
                }
                const row = window.appFilteredRows[index];
                
                let safeInt = (v) => { let p = parseInt(v); return isNaN(p) ? 0 : p; };
                let safeFloat = (v) => { let p = parseFloat(v); return isNaN(p) ? 0 : p; };
                
                let base = row['BASE'] ? row['BASE'].trim().toUpperCase() : 'CORE';
                let bateu = safeFloat(row['BATEU META']);
                
                let falta_volume_app = "";
                if (base === 'HIGH END' && bateu === 0) {
                    let m_600 = safeInt(row['META 600 HE']); let r_600 = safeInt(row['REAL 600 HE']);
                    let m_ln = safeInt(row['META LN']); let r_ln = safeInt(row['REAL LN']);
                    let m_lnz = safeInt(row['META LN ZERO']); let r_lnz = safeInt(row['REAL LN ZERO']);
                    let faltas = [];
                    if (r_600 < m_600) faltas.push((m_600 - r_600) + " cx de 600ml");
                    if (r_ln < m_ln) faltas.push((m_ln - r_ln) + " cx de Long Neck");
                    if (r_lnz < m_lnz) faltas.push((m_lnz - r_lnz) + " cx de Long Neck Zero");
                    if (faltas.length > 0) falta_volume_app = "Falta vender " + faltas.join(" + ") + ".";
                } else if (bateu === 0) {
                    let m_int = safeInt(row['META 600']); let r_int = safeInt(row['REAL 600']);
                    let m_rgb = safeInt(row['META RGB']); let r_rgb = safeInt(row['REAL RGB']);
                    let m_300 = safeInt(row['META 300']); let r_300 = safeInt(row['REAL 300']);
                    let faltas = [];
                    if (r_int < m_int) faltas.push((m_int - r_int) + " cx de Inteira (600ml)");
                    if (r_rgb < m_rgb) faltas.push((m_rgb - r_rgb) + " cx de RGB");
                    if (r_300 < m_300) faltas.push((m_300 - r_300) + " cx de 300ml");
                    if (faltas.length > 0) falta_volume_app = "Falta vender " + faltas.join(" + ") + ".";
                }
                
                // Tratar valores monetários BRL (ex: "3.010,00" -> 3010)
                let parseBRL = (val) => {
                    if (!val) return 0;
                    if (typeof val === 'number') return val;
                    let str = val.toString().trim();
                    if (str === '-' || str === '') return 0;
                    str = str.replace(/\\./g, '');
                    str = str.replace(',', '.');
                    let num = parseFloat(str);
                    return isNaN(num) ? 0 : num;
                };

                const data = {
                    nome: row['NOME PDV'] || 'Cliente',
                    comprador: safeInt(row['COMPR']),
                    possui_task: row['POSSUI TASK'] ? row['POSSUI TASK'].trim().toUpperCase() : 'N',
                    meta_task: parseBRL(row['META TASK']),
                    real_task: parseBRL(row['REAL TASK']),
                    coolers: safeInt(row['COOLERS']),
                    falta_volume: falta_volume_app
                };
                
                window.pdvContextoCopiloto = data;
                
                const clienteInput = document.getElementById('cliente');
                if (clienteInput) clienteInput.value = data.nome;
                
                const copilotSection = document.getElementById('copiloto-section');
                if (copilotSection) copilotSection.scrollIntoView({ behavior: 'smooth' });
                
                setTimeout(() => {
                    const btnGen = document.getElementById('generate-btn');
                    if (btnGen) {
                        btnGen.click();
                    } else {
                        alert("Erro: Botão de geração (generate-btn) não encontrado na tela!");
                    }
                }, 600);
            } catch(e) {
                alert("Erro ao preparar dados da IA: " + e.message);
                console.error(e);
            }
        };"""
        
    html = html.replace(target_script, chamar_copiloto_fn, 1)

    # 2. Add window.appFilteredRows before the loop
    target_loop = "filteredRows.forEach(row => {"
    replacement_loop = """window.appFilteredRows = filteredRows;
                filteredRows.forEach((row, index) => {"""
    html = html.replace(target_loop, replacement_loop)

    # 3. Replace the data encoding with a simple onclick index
    target_data_str = """let copiloto_data_str = encodeURIComponent(JSON.stringify({
                        nome: row['NOME PDV'],
                        comprador: comprador,
                        possui_task: possui_task,
                        meta_task: meta_task,
                        real_task: real_task,
                        coolers: coolers,
                        falta_volume: falta_volume_app
                    })).replace(/'/g, "%27");"""
    
    html = html.replace(target_data_str, "/* copiloto_data_str removido, usando index agora */")

    # 4. Replace the onclick in the button
    html = html.replace("onclick=\"prepararCopiloto('${copiloto_data_str}')\"", "onclick=\"chamarCopiloto(${index})\"")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Bump service worker cache again to be 100% sure
    with open('sw.js', 'r', encoding='utf-8') as f:
        sw = f.read()
    sw = re.sub(r"const CACHE_NAME = 'dmc-copilot-v\d+';", "const CACHE_NAME = 'dmc-copilot-v11';", sw)
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(sw)

if __name__ == '__main__':
    patch()
