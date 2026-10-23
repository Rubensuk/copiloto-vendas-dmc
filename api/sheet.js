import Papa from 'papaparse';

export default async function handler(req, res) {
    try {
        // urlPortf (1IHbn...): Planilha de Portfólio / Mix de Produtos / Metas de Volume (600, Inteira, RGB, etc.)
        const urlPortf = 'https://docs.google.com/spreadsheets/d/1IHbnIjofO3ozVBrywfb4bzGUsktE3Fu0/export?format=csv&gid=378465162';
        
        // urlExec (1xiDa...): Planilha de Execução Score 5, Trade, Comodatos (Coolers) e Faturamento (Meta, Real)
        const urlExec = 'https://docs.google.com/spreadsheets/d/1xiDaCjqnlurP-YKXH3RYohyVL-bT1G3K/export?format=csv&gid=1748584987';
        
        // Faz o download das duas planilhas em paralelo
        const [resPortf, resExec] = await Promise.all([
            fetch(urlPortf),
            fetch(urlExec)
        ]);
        
        if (!resPortf.ok || !resExec.ok) {
            return res.status(500).json({ error: 'Erro ao acessar planilhas no Google Drive' });
        }
        
        let csvPortf = await resPortf.text();
        let csvExec = await resExec.text();
        
        // --- 1. TRATAMENTO DE CABEÇALHOS DUPLICADOS DO PORTFÓLIO (csvPortf) ---
        let linesPortf = csvPortf.split(/\r?\n/);
        if (linesPortf.length > 0) {
            let headers = linesPortf[0].split(',');
            for(let i = 20; i <= 36; i++) {
                if(headers[i]) {
                    let clean = headers[i].trim().replace(/^["']|["']$/g, '');
                    headers[i] = clean ? `HE_${clean}` : headers[i];
                }
            }
            for(let i = 37; i <= 57; i++) {
                if(headers[i]) {
                    let clean = headers[i].trim().replace(/^["']|["']$/g, '');
                    headers[i] = clean ? `CORE_${clean}` : headers[i];
                }
            }
            linesPortf[0] = headers.join(',');
            csvPortf = linesPortf.join('\n');
        }
        
        // --- 2. PARSE DAS PLANILHAS ---
        const parsedPortf = Papa.parse(csvPortf, { header: true, skipEmptyLines: true });
        const parsedExec = Papa.parse(csvExec, { header: true, skipEmptyLines: true });
        
        function normChave(val) {
            if (!val) return '';
            let s = String(val).trim().replace(/^["']|["']$/g, '');
            s = s.replace(/\.0+$/, '');
            return s.trim();
        }

        function normNome(val) {
            if (!val) return '';
            return String(val).trim().toUpperCase().replace(/["']/g, '').replace(/\s+/g, ' ');
        }

        // Indexar a planilha de Execução por chave e por nome
        const dictExec = {};
        const dictExecByNome = {};

        for (const row of parsedExec.data) {
            const rawChave = row['CHAVE PDV'] || row['CHAVE'] || row['COD_PDV'] || row['COD PDV'];
            if (rawChave !== undefined && rawChave !== null) {
                const trimmed = String(rawChave).trim();
                const cleanQuotes = trimmed.replace(/^["']|["']$/g, '');
                const norm = normChave(trimmed);
                if (trimmed) dictExec[trimmed] = row;
                if (cleanQuotes) dictExec[cleanQuotes] = row;
                if (norm) dictExec[norm] = row;
            }
            const rawNome = row['NOME PDV'] || row['NOME'] || row['CLIENTE'] || row['RAZAO SOCIAL'];
            if (rawNome) {
                const nn = normNome(rawNome);
                if (nn) dictExecByNome[nn] = row;
            }
        }
        
        const execHeaders = parsedExec.meta.fields || [];
        const ignoreHeaders = ['CHAVE PDV', 'NOME PDV', 'GEO', 'RN', 'COMERCIAL', 'OPERAÇÃO', 'GV', 'VISITA', 'BASE', 'id_ano_mes'];
        
        const parseNum = (v) => {
            if (!v) return 0;
            let s = String(v).replace(/\s/g, '').replace(/^R\$/i, '').trim();
            if (s.includes(',') && s.includes('.')) {
                s = s.replace(/\./g, '').replace(',', '.');
            } else if (s.includes(',')) {
                s = s.replace(',', '.');
            } else if (s.includes('.')) {
                const parts = s.split('.');
                if (parts.length === 2 && parts[1].length === 3) {
                    s = parts[0] + parts[1];
                }
            }
            const n = parseFloat(s);
            return isNaN(n) ? 0 : n;
        };

        // Mesclar dados de Execução e Faturamento na base de Portfólio
        for (let row of parsedPortf.data) {
            const rawChave = row['CHAVE PDV'] || row['COD_PDV'] || row['COD PDV'];
            const chave = rawChave ? String(rawChave).trim() : null;
            const rawNome = row['NOME PDV'] || row['CLIENTE'];
            const nn = rawNome ? normNome(rawNome) : null;

            const execData = chave ? (dictExec[chave] || dictExec[normChave(chave)] || dictExec[chave.replace(/^["']|["']$/g, '')]) : (nn ? dictExecByNome[nn] : null);
            
            // Garantir que todos os campos de execução existam na row
            for (const h of execHeaders) {
                const cleanH = h.replace(/["']/g, '').trim();
                if (!ignoreHeaders.includes(cleanH) && !ignoreHeaders.includes(h)) {
                    const val = execData ? (execData[h] !== undefined ? execData[h] : execData[cleanH]) : '';
                    row[cleanH] = val !== undefined && val !== null ? val : '';
                }
            }

            // Normalização explícita dos campos vitais de execução e trade
            const camposVitais = ['COOLERS', 'MAT TRADE', 'MENU & PTC', 'MENU', 'DIG COUP', 'VISITAÇÃO', 'QTDE VISITAS', 'PTs', 'COMPR', 'CERV (TEND)', 'HE (TEND)'];
            for (const cv of camposVitais) {
                if (row[cv] === undefined || row[cv] === null) {
                    const val = execData ? execData[cv] : '';
                    row[cv] = val !== undefined && val !== null ? val : '';
                }
            }

            // Normalização de Faturamento (Meta, Real, Gap, Possui Task)
            const metaVal = (row['META TASK'] !== undefined && row['META TASK'] !== null && String(row['META TASK']).trim() !== '') 
                ? String(row['META TASK']).trim() 
                : (execData && (execData['META TASK'] || execData['META'] || execData['META FAT'] || execData['META FATURAMENTO'] || execData['OBJETIVO'])) || '';

            const realVal = (row['REAL TASK'] !== undefined && row['REAL TASK'] !== null && String(row['REAL TASK']).trim() !== '') 
                ? String(row['REAL TASK']).trim() 
                : (execData && (execData['REAL TASK'] || execData['REAL'] || execData['REALIZADO'] || execData['REAL FAT'] || execData['FATURAMENTO'])) || '';

            const metaNum = parseNum(metaVal);
            const realNum = parseNum(realVal);
            const gapCalc = Math.max(0, metaNum - realNum);

            const gapVal = (row['GAP TASK'] !== undefined && row['GAP TASK'] !== null && String(row['GAP TASK']).trim() !== '')
                ? String(row['GAP TASK']).trim()
                : (execData && (execData['GAP TASK'] || execData['GAP'] || execData['FALTA'])) || (metaNum > 0 ? String(gapCalc) : '0');

            row['META TASK'] = metaVal;
            row['META'] = metaVal;
            row['REAL TASK'] = realVal;
            row['REAL'] = realVal;
            row['GAP TASK'] = gapVal;
            row['GAP'] = gapVal;

            const possuiVal = (row['POSSUI TASK'] !== undefined && row['POSSUI TASK'] !== null && String(row['POSSUI TASK']).trim() !== '')
                ? String(row['POSSUI TASK']).trim()
                : (execData && execData['POSSUI TASK']) || ((metaNum > 0 || realNum > 0) ? 'S' : '');

            row['POSSUI TASK'] = possuiVal;
        }

        // Montar a lista definitiva de todas as colunas unificadas para garantir a integridade do CSV
        const allFieldsSet = new Set(parsedPortf.meta.fields || []);
        ['COOLERS', 'MAT TRADE', 'MENU & PTC', 'MENU', 'DIG COUP', 'VISITAÇÃO', 'QTDE VISITAS', 'PTs', 'COMPR', 'CERV (TEND)', 'HE (TEND)', 'META TASK', 'META', 'REAL TASK', 'REAL', 'GAP TASK', 'GAP', 'POSSUI TASK'].forEach(f => allFieldsSet.add(f));
        execHeaders.forEach(f => {
            const clean = f.replace(/["']/g, '').trim();
            if (!ignoreHeaders.includes(clean)) allFieldsSet.add(clean);
        });

        const finalCsv = Papa.unparse({
            fields: Array.from(allFieldsSet),
            data: parsedPortf.data
        });
        
        res.setHeader('Content-Type', 'text/csv; charset=utf-8');
        res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(finalCsv);
    } catch (error) {
        console.error('Erro na API:', error);
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
