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
        
        // --- TRATAMENTO DE CABEÇALHOS DUPLICADOS DA BASE ---
        let lines = csvBase.split(/\r?\n/);
        if (lines.length > 0) {
            let headers = lines[0].split(',');
            // Índices 19 a 35 são High End (SPT 600 até OUTROS LN ZERO)
            for(let i = 19; i <= 35; i++) {
                if(headers[i]) {
                    let clean = headers[i].trim().replace(/^["']|["']$/g, '');
                    headers[i] = clean ? `HE_${clean}` : headers[i];
                }
            }
            // Índices 36 a 56 são Core (AP 600 até OUTROS 1000)
            for(let i = 36; i <= 56; i++) {
                if(headers[i]) {
                    let clean = headers[i].trim().replace(/^["']|["']$/g, '');
                    headers[i] = clean ? `CORE_${clean}` : headers[i];
                }
            }
            lines[0] = headers.join(',');
            csvBase = lines.join('\n');
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

        // Identificar dinamicamente o campo de chave no Faturamento
        const fatHeaders = parsedFat.meta.fields || [];
        const fatChaveField = fatHeaders.find(f => {
            const clean = f.replace(/["']/g, '').trim().toUpperCase();
            return clean === 'CHAVE PDV' || clean === 'CHAVE' || clean === 'COD_PDV' || clean === 'COD PDV' || clean === 'CODIGO';
        }) || 'CHAVE PDV';

        // Indexar a planilha de Faturamento por múltiplas variações da chave
        const dictFat = {};
        for (const row of parsedFat.data) {
            const rawVal = row[fatChaveField] || row['CHAVE PDV'];
            if (rawVal !== undefined && rawVal !== null) {
                const trimmed = String(rawVal).trim();
                const cleanQuotes = trimmed.replace(/^["']|["']$/g, '');
                const norm = normChave(trimmed);
                if (trimmed) dictFat[trimmed] = row;
                if (cleanQuotes) dictFat[cleanQuotes] = row;
                if (norm) dictFat[norm] = row;
            }
        }
        
        // Identificar colunas do Faturamento que serão unidas (evitando duplicar chaves primárias)
        const ignoreHeaders = ['CHAVE PDV', 'NOME PDV', 'GEO', 'RN', 'COMERCIAL', 'OPERAÇÃO', 'GV', 'VISITA', 'BASE', 'id_ano_mes'];
        
        // Cruzar os dados da Base com o Faturamento
        for (let row of parsedBase.data) {
            const rawChave = row['CHAVE PDV'];
            const chave = rawChave ? String(rawChave).trim() : null;
            const fatData = chave ? (dictFat[chave] || dictFat[normChave(chave)] || dictFat[chave.replace(/^["']|["']$/g, '')]) : null;
            
            for (const h of fatHeaders) {
                const cleanH = h.replace(/["']/g, '').trim();
                if (!ignoreHeaders.includes(cleanH) && !ignoreHeaders.includes(h)) {
                    const val = fatData ? (fatData[h] !== undefined ? fatData[h] : fatData[cleanH]) : '';
                    row[cleanH] = val !== undefined && val !== null ? val : '';
                }
            }
        }
        
        // Reverter o JSON mesclado de volta para CSV (mantendo a mesma interface para o Front-end)
        const finalCsv = Papa.unparse(parsedBase.data);
        
        res.setHeader('Content-Type', 'text/csv; charset=utf-8');
        res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=60');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(finalCsv);
    } catch (error) {
        console.error('Erro na API:', error);
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
