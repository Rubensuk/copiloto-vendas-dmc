import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target = """                    // --- NOVOS DADOS DE FATURAMENTO E EXECUÇÃO ---
                    let meta_task = parseFloat(row['META TASK']) || 0;
                    let real_task = parseFloat(row['REAL TASK']) || 0;"""

    replacement = """                    // --- NOVOS DADOS DE FATURAMENTO E EXECUÇÃO ---
                    function parseBRL(val) {
                        if (!val) return 0;
                        let clean = String(val).replace(/\\./g, '').replace(',', '.');
                        return parseFloat(clean) || 0;
                    }
                    let meta_task = parseBRL(row['META TASK']);
                    let real_task = parseBRL(row['REAL TASK']);"""

    html = html.replace(target, replacement)

    target_bar = """if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        fat_html += barraHTML(pct_task, `💪 Desafio BEES Force — Meta: R$ ${meta_task.toFixed(2)} | Real: R$ ${real_task.toFixed(2)} | Falta: R$ ${Math.max(0, meta_task - real_task).toFixed(2)}`);
                    } else {"""

    replacement_bar = """if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        let formatBRL = (v) => v.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                        fat_html += barraHTML(pct_task, `💪 Desafio BEES Force — Meta: R$ ${formatBRL(meta_task)} | Real: R$ ${formatBRL(real_task)} | Falta: R$ ${formatBRL(Math.max(0, meta_task - real_task))}`);
                    } else {"""

    html = html.replace(target_bar, replacement_bar)
    
    # Also fix the copilot injection where it calculates "falta"
    target_copilot = """let falta_rs = (pdv.meta_task - pdv.real_task).toFixed(2);"""
    replacement_copilot = """let falta_rs = (pdv.meta_task - pdv.real_task).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});"""
    html = html.replace(target_copilot, replacement_copilot)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
