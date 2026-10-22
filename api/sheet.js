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
        // A planilha de portfólio possui cabeçalhos com o mesmo nome para High End e Core:
        // Índices 20 a 36 são High End (SPT 600 até OUTROS LN ZERO) -> prefixar com HE_
        // Índices 37 a 57 são Core (AP 600 até OUTROS 1000) -> prefixar com CORE_
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
        // --- FIM DO TRATAMENTO ---
        
        // --- 2. PARSE DAS PLANILHAS ---
        // csvExec é a planilha de Execução e Faturamento (suas colunas originais são preservadas intactas!)
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
        
        // Colunas da Execução que serão adicionadas a cada PDV do Portfólio
        const execHeaders = parsedExec.meta.fields || [];
        const ignoreHeaders = ['CHAVE PDV', 'NOME PDV', 'GEO', 'RN', 'COMERCIAL', 'OPERAÇÃO', 'GV', 'VISITA', 'BASE', 'id_ano_mes'];
        
        // Função para converter strings de valor para número com suporte a milhar
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

        // Mesclar dados de Execução e Faturamento na base de Portfólio (que contém todos os PDVs cadastrados)
        for (let row of parsedPortf.data) {
            const rawChave = row['CHAVE PDV'] || row['COD_PDV'] || row['COD PDV'];
            const chave = rawChave ? String(rawChave).trim() : null;
            const rawNome = row['NOME PDV'] || row['CLIENTE'];
            const nn = rawNome ? normNome(rawNome) : null;

            // Busca na Execução por chave ou fallback por nome
            const execData = chave ? (dictExec[chave] || dictExec[normChave(chave)] || dictExec[chave.replace(/^["']|["']$/g, '')]) : (nn ? dictExecByNome[nn] : null);
            
            if (execData) {
                for (const h of execHeaders) {
                    const cleanH = h.replace(/["']/g, '').trim();
                    if (!ignoreHeaders.includes(cleanH) && !ignoreHeaders.includes(h)) {
                        const val = execData[h] !== undefined ? execData[h] : execData[cleanH];
                        row[cleanH] = val !== undefined && val !== null ? val : '';
                    }
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
        
        // Reverter o JSON mesclado de volta para CSV (mantendo a mesma interface para o Front-end)
        const finalCsv = Papa.unparse(parsedPortf.data);
        
        res.setHeader('Content-Type', 'text/csv; charset=utf-8');
        res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(finalCsv);
    } catch (error) {
        console.error('Erro na API:', error);
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
