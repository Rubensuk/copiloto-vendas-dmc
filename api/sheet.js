export default async function handler(req, res) {
    try {
        const url = 'https://docs.google.com/spreadsheets/d/1I7mM2zzqLABFnxi2Lx_-Sk86HrvmCRvv/export?format=csv&gid=1015537580';
        const response = await fetch(url);
        
        if (!response.ok) {
            return res.status(response.status).json({ error: 'Erro ao acessar Google Drive' });
        }
        
        const csvText = await response.text();
        
        // Retorna o CSV bruto para o frontend processar (ou poderíamos parsear aqui)
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).send(csvText);
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ error: 'Erro interno no servidor' });
    }
}
