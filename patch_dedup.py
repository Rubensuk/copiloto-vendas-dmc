import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target = """                            if (!consolidado[rn]) {
                                consolidado[rn] = { pdvs: 0, meta: 0, kpis_ok_sum: 0, rows: [] };
                            }

                            consolidado[rn].pdvs += 1;
                            consolidado[rn].rows.push(row);"""

    replacement = """                            if (!consolidado[rn]) {
                                consolidado[rn] = { pdvs: 0, meta: 0, kpis_ok_sum: 0, rows: [], _chaves: new Set() };
                            }
                            
                            const chave = row['CHAVE PDV'];
                            if (chave) {
                                if (consolidado[rn]._chaves.has(chave)) return; // Ignora duplicatas exatas
                                consolidado[rn]._chaves.add(chave);
                            }

                            consolidado[rn].pdvs += 1;
                            consolidado[rn].rows.push(row);"""

    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
