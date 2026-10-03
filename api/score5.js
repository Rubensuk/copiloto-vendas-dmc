import Papa from 'papaparse';

export default async function handler(req, res) {
    try {
        const urlScore5 = process.env.NEXT_PUBLIC_SCORE5_CSV_URL || 'https://docs.google.com/spreadsheets/d/1usFqbU3-WEahjVbeAFXmOdv2q2-Y_FXz/export?format=csv&gid=377036402';
        
        const response = await fetch(urlScore5);
        if (!response.ok) {
            return res.status(500).json({ error: 'Erro ao acessar planilha de Score 5 no Google Drive' });
        }
        
        const csvData = await response.text();
        const parsed = Papa.parse(csvData, { header: true, skipEmptyLines: true });
        
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=60');
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.status(200).json({
            success: true,
            totalRows: parsed.data.length,
            data: parsed.data
        });
    } catch (error) {
        console.error('Erro na API de Score 5:', error);
        res.status(500).json({ error: 'Erro interno ao consultar dados do Score 5' });
    }
}
