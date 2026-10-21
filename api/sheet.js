import Papa from 'papaparse';

export default async function handler(req, res) {
    try {
        const urlBase = 'https://docs.google.com/spreadsheets/d/1IHbnIjofO3ozVBrywfb4bzGUsktE3Fu0/export?format=csv&gid=378465162';
        const urlFat = 'https://docs.google.com/spreadsheets/d/1xiDaCjqnlurP-YKXH3RYohyVL-bT1G3K/export?format=csv&gid=1748584987';
        
        // Faz o download das duas planilhas em paralelo
        const [resBase, resFat] = await Promise.all([
            fetch(urlBase),
            fetch(urlFat)
        ]);
        
        if (!resBase.ok || !resFat.ok) {
            return res.status(500).json({ error: 'Erro ao acessar planilhas no Google Drive' });
        }
        
        let csvBase = await resBase.text();
        let csvFat = await resFat.text();
        
        // --- TRATAMENTO DE CABEÇALHOS DUPLICADOS DO PORTFÓLIO (csvFat) ---
        let linesFat = csvFat.split(/\r?\n/);
        if (linesFat.length > 0) {
            let headers = linesFat[0].split(',');
            // Índices 20 a 36 são High End (SPT 600 até OUTROS LN ZERO)
            for(let i = 20; i <= 36; i++) {
                if(headers[i]) {
                    let clean = headers[i].trim().replace(/^["']|["']$/g, '');
                    headers[i] = clean ? `HE_${clean}` : headers[i];
                }
            }
            // Índices 37 a 57 são Core (AP 600 até OUTROS 1000)
            for(let i = 37; i <= 57; i++) {
                if(headers[i]) {
                    let clean = headers[i].trim().replace(/^["']|["']$/g, '');
                    headers[i] = clean ? `CORE_${clean}` : headers[i];
                }
            }
            linesFat[0] = headers.join(',');
            csvFat = linesFat.join('\n');
        }
        // --- FIM DO TRATAMENTO ---
        
        // Fazer o parse de ambas as planilhas
        const parsedBase = Papa.parse(csvBase, { header: true, skipEmptyLines: true });
        const parsedFat = Papa.parse(csvFat, { header: true, skipEmptyLines: true });
        
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

        const fatHeaders = parsedFat.meta.fields || [];
        const fatChaveField = fatHeaders.find(f => {
            const clean = f.replace(/["']/g, '').trim().toUpperCase();
            return clean === 'CHAVE PDV' || clean === 'CHAVE' || clean === 'COD_PDV' || clean === 'COD PDV' || clean === 'CODIGO';
        }) || 'CHAVE PDV';

        const fatNomeField = fatHeaders.find(f => {
            const clean = f.replace(/["']/g, '').trim().toUpperCase();
            return clean === 'NOME PDV' || clean === 'NOME' || clean === 'CLIENTE' || clean === 'RAZAO SOCIAL';
        }) || 'NOME PDV';

        // Indexar a planilha de Faturamento por chave E por nome
        const dictFat = {};
        const dictFatByNome = {};

        for (const row of parsedFat.data) {
            const rawChave = row[fatChaveField] || row['CHAVE PDV'];
            if (rawChave !== undefined && rawChave !== null) {
                const trimmed = String(rawChave).trim();
                const cleanQuotes = trimmed.replace(/^["']|["']$/g, '');
                const norm = normChave(trimmed);
                if (trimmed) dictFat[trimmed] = row;
                if (cleanQuotes) dictFat[cleanQuotes] = row;
                if (norm) dictFat[norm] = row;
            }
            const rawNome = row[fatNomeField] || row['NOME PDV'];
            if (rawNome) {
                const nn = normNome(rawNome);
                if (nn) dictFatByNome[nn] = row;
            }
        }
        
        // Identificar colunas do Faturamento que serão unidas (evitando duplicar chaves primárias)
        const ignoreHeaders = ['CHAVE PDV', 'NOME PDV', 'GEO', 'RN', 'COMERCIAL', 'OPERAÇÃO', 'GV', 'VISITA', 'BASE', 'id_ano_mes'];
        
        // Cruzar os dados da Base com o Portfólio / Faturamento
        for (let row of parsedBase.data) {
            const rawChave = row['CHAVE PDV'] || row['COD_PDV'] || row['COD PDV'];
            const chave = rawChave ? String(rawChave).trim() : null;
            const rawNome = row['NOME PDV'] || row['CLIENTE'];
            const nn = rawNome ? normNome(rawNome) : null;

            // Busca por chave ou fallback por nome
            const fatData = chave ? (dictFat[chave] || dictFat[normChave(chave)] || dictFat[chave.replace(/^["']|["']$/g, '')]) : (nn ? dictFatByNome[nn] : null);
            
            if (fatData) {
                for (const h of fatHeaders) {
                    const cleanH = h.replace(/["']/g, '').trim();
                    if (!ignoreHeaders.includes(cleanH) && !ignoreHeaders.includes(h)) {
                        const val = fatData[h] !== undefined ? fatData[h] : fatData[cleanH];
                        row[cleanH] = val !== undefined && val !== null ? val : '';
                    }
                }
            }

            // Normalização de Faturamento (Meta, Real, Gap, Possui Task)
            // A planilha Base é a fonte principal de Meta e Real Task
            const metaVal = (row['META TASK'] !== undefined && row['META TASK'] !== null && String(row['META TASK']).trim() !== '') 
                ? String(row['META TASK']).trim() 
                : (row['META'] || (fatData && (fatData['META TASK'] || fatData['META'] || fatData['META FAT'] || fatData['META FATURAMENTO'] || fatData['OBJETIVO'])) || '');

            const realVal = (row['REAL TASK'] !== undefined && row['REAL TASK'] !== null && String(row['REAL TASK']).trim() !== '') 
                ? String(row['REAL TASK']).trim() 
                : (row['REAL'] || (fatData && (fatData['REAL TASK'] || fatData['REAL'] || fatData['REALIZADO'] || fatData['REAL FAT'] || fatData['FATURAMENTO'])) || '');

            const parseNum = (v) => {
                if (!v) return 0;
                let s = String(v).replace(/\s/g, '').replace(/^R\$/i, '').trim();
                if (s.includes(',') && s.includes('.')) {
                    s = s.replace(/\./g, '').replace(',', '.');
                } else if (s.includes(',')) {
                    s = s.replace(',', '.');
                }
                const n = parseFloat(s);
                return isNaN(n) ? 0 : n;
            };

            const metaNum = parseNum(metaVal);
            const realNum = parseNum(realVal);
            const gapCalc = Math.max(0, metaNum - realNum);

            const gapVal = (row['GAP TASK'] !== undefined && row['GAP TASK'] !== null && String(row['GAP TASK']).trim() !== '')
                ? String(row['GAP TASK']).trim()
                : (row['GAP'] || (fatData && (fatData['GAP TASK'] || fatData['GAP'] || fatData['FALTA'])) || (metaNum > 0 ? String(gapCalc) : '0'));

            row['META TASK'] = metaVal;
            row['META'] = metaVal;
            row['REAL TASK'] = realVal;
            row['REAL'] = realVal;
            row['GAP TASK'] = gapVal;
            row['GAP'] = gapVal;

            const possuiVal = (row['POSSUI TASK'] !== undefined && row['POSSUI TASK'] !== null && String(row['POSSUI TASK']).trim() !== '')
                ? String(row['POSSUI TASK']).trim()
                : (fatData && fatData['POSSUI TASK']) || ((metaNum > 0 || realNum > 0) ? 'S' : '');

            row['POSSUI TASK'] = possuiVal;
        }
        
        // Reverter o JSON mesclado de volta para CSV (mantendo a mesma interface para o Front-end)
        const finalCsv = Papa.unparse(parsedBase.data);
        
        res.setHeader('Content-Type', 'text/csv; charset=utf-8');
        res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(finalCsv);
    } catch (error) {
        console.error('Erro na API:', error);
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
