export default async function handler(req, res) {
    try {
        const url = 'https://docs.google.com/spreadsheets/d/1IHbnIjofO3ozVBrywfb4bzGUsktE3Fu0/export?format=csv&gid=378465162';
        const response = await fetch(url);
        
        if (!response.ok) {
            return res.status(response.status).json({ error: 'Erro ao acessar Google Drive' });
        }
        
        
        let csvText = await response.text();
        
        // --- INÍCIO DO TRATAMENTO DE CABEÇALHOS DUPLICADOS ---
        let lines = csvText.split(/\r?\n/);
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
            csvText = lines.join('\n');
        }
        // --- FIM DO TRATAMENTO ---
        
        
        // Retorna o CSV bruto para o frontend processar (ou poderíamos parsear aqui)
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=60');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(csvText);
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
