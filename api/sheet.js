export default async function handler(req, res) {
    try {
        const url = 'https://docs.google.com/spreadsheets/d/1WJOSePDmcVRjANuUXIuJLFdB8p0yhTvB/export?format=csv';
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
