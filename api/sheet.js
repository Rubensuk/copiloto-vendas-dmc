export default async function handler(req, res) {
    try {
        const url = 'https://docs.google.com/spreadsheets/d/1IHbnIjofO3ozVBrywfb4bzGUsktE3Fu0/export?format=csv&gid=378465162';
        const response = await fetch(url);
        
        if (!response.ok) {
            return res.status(response.status).json({ error: 'Erro ao acessar Google Drive' });
        }
        
        const csvText = await response.text();
        
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
