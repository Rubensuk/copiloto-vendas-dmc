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
                if(headers[i]) headers[i] = 'HE_' + headers[i].trim();
            }
            // Índices 36 a 56 são Core (AP 600 até OUTROS 1000)
            for(let i = 36; i <= 56; i++) {
                if(headers[i]) headers[i] = 'CORE_' + headers[i].trim();
            }
            lines[0] = headers.join(',');
            csvBase = lines.join('\n');
        }
        // --- FIM DO TRATAMENTO ---
        
        // Fazer o parse de ambas as planilhas
        const parsedBase = Papa.parse(csvBase, { header: true, skipEmptyLines: true });
        const parsedFat = Papa.parse(csvFat, { header: true, skipEmptyLines: true });
        
        // Indexar a planilha de Faturamento pela CHAVE PDV para cruzamento rápido
        const dictFat = {};
        for (const row of parsedFat.data) {
            if (row['CHAVE PDV']) {
                dictFat[row['CHAVE PDV'].trim()] = row;
            }
        }
        
        // Identificar colunas do Faturamento que serão unidas (evitando duplicar chaves primárias)
        const fatHeaders = parsedFat.meta.fields || [];
        const ignoreHeaders = ['CHAVE PDV', 'NOME PDV', 'GEO', 'RN', 'COMERCIAL', 'OPERAÇÃO', 'GV', 'VISITA', 'BASE', 'id_ano_mes'];
        
        // Cruzar os dados da Base com o Faturamento
        for (let row of parsedBase.data) {
            const chave = row['CHAVE PDV'] ? row['CHAVE PDV'].trim() : null;
            const fatData = chave ? dictFat[chave] : null;
            
            for (const h of fatHeaders) {
                if (!ignoreHeaders.includes(h)) {
                    row[h] = fatData && fatData[h] !== undefined ? fatData[h] : '';
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
