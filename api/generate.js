// generate.js – serverless function (Node.js) with Resilient Retry & Fallback
// ---------------------------------------------------------------------------------
// Deployed on Vercel Serverless Functions.
// Handles CORS, automatic retries on 503/429 status codes, and intelligent model fallback.

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default async function handler(req, res) {
  // Configuração de cabeçalhos CORS para permitir acesso local/externo
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Responde imediatamente a requisições preflight OPTIONS
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  // Parse seguro do corpo da requisição
  let prompt;
  if (req.body && typeof req.body === 'object') {
    ({ prompt } = req.body);
  } else {
    try {
      const raw = await new Promise((resolve, reject) => {
        let data = '';
        req.on('data', (chunk) => (data += chunk));
        req.on('end', () => resolve(data));
        req.on('error', reject);
      });
      const parsed = JSON.parse(raw || '{}');
      prompt = parsed.prompt;
    } catch (_) {
      // keep prompt undefined
    }
  }

  if (!prompt) {
    return res.status(400).json({ error: 'Missing prompt' });
  }

  const PROVIDER = process.env.AI_PROVIDER || 'gemini';
  const API_KEY = process.env.AI_API_KEY;

  if (!API_KEY) {
    return res.status(500).json({ error: 'AI_API_KEY is not configured in Vercel environment variables.' });
  }

  // Lista de modelos resilientes para fallback em caso de sobrecarga (503/429)
  const GEMINI_MODELS = ['gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.6-flash'];
  let lastError = null;

  if (PROVIDER === 'gemini') {
    const payload = { contents: [{ role: 'user', parts: [{ text: prompt }] }] };

    for (const model of GEMINI_MODELS) {
      const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${API_KEY}`;
      
      // Realiza até 2 tentativas por modelo com backoff curto
      for (let attempt = 1; attempt <= 2; attempt++) {
        try {
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });

          if (response.ok) {
            const data = await response.json();
            const result = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
            return res.status(200).json({ result, modelUsed: model });
          }

          const errText = await response.text();
          lastError = new Error(`Model ${model} returned ${response.status}: ${errText}`);

          // Se for erro 503 (sobrecarga temporária) ou 429 (rate limit), aguarda e tenta novamente
          if (response.status === 503 || response.status === 429) {
            await sleep(800 * attempt);
            continue; // próxima tentativa
          } else {
            // Se for outro tipo de erro (ex: 404), vai direto para o próximo modelo de fallback
            break;
          }
        } catch (fetchErr) {
          lastError = fetchErr;
          await sleep(500);
        }
      }
    }

    console.error('All Gemini fallback models exhausted. Last error:', lastError);
    return res.status(503).json({ 
      error: lastError ? lastError.message : 'Todos os modelos do Gemini estão temporariamente indisponíveis. Tente novamente em alguns instantes.' 
    });
  } else {
    // Provedor OpenAI
    try {
      const payload = {
        model: 'gpt-3.5-turbo',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7,
      };

      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${API_KEY}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(`OpenAI API error ${response.status}: ${err}`);
      }

      const data = await response.json();
      const result = data.choices?.[0]?.message?.content || '';
      return res.status(200).json({ result });
    } catch (e) {
      console.error('OpenAI error:', e);
      return res.status(500).json({ error: e.message });
    }
  }
}
