import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Personas with initialMessage
    old_personas = r"const PERSONAS = \[\s*\{\s*id: 'zeca',.*?desc: '60 anos.*?prompt: `Você é \"Zeca\".*?\} \];"
    # Actually it's better to just replace the whole PERSONAS block using a robust regex or string slicing.
    
    # We will use re.sub to inject initialMessage for each persona.
    html = html.replace(
        "id: 'zeca',\n            name: 'Zeca",
        "initialMessage: 'Oi. O que você quer hoje? Já adianto que estou sem tempo.',\n            id: 'zeca',\n            name: 'Zeca"
    )
    html = html.replace(
        "id: 'bibi',\n            name: 'Bibi",
        "initialMessage: 'Olá. Se for para oferecer produto novo, já aviso que estou sem espaço na geladeira.',\n            id: 'bibi',\n            name: 'Bibi"
    )
    html = html.replace(
        "id: 'joao',\n            name: 'João",
        "initialMessage: 'Fala, campeão! Tudo bem? Hoje o movimento tá meio devagar por aqui...',\n            id: 'joao',\n            name: 'João"
    )
    html = html.replace(
        "id: 'marcos',\n            name: 'Marcos",
        "initialMessage: 'E aí... Escuta, aquele último pedido veio com o boleto muito curto, viu?',\n            id: 'marcos',\n            name: 'Marcos"
    )

    # 2. Update startSimulation to use initialMessage
    old_start = "addMessage('bot', 'Oi. O que você quer hoje? Já adianto que estou sem tempo.');"
    new_start = "addMessage('bot', currentPersona.initialMessage);"
    html = html.replace(old_start, new_start)

    # 3. Update API_URL logic for localhost/file protocol testing
    old_api = "const API_URL = '/api/generate';"
    new_api = """let API_URL = '/api/generate';
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.protocol === "file:") {
        API_URL = "https://dmc-copilot.vercel.app/api/generate";
    }"""
    html = html.replace(old_api, new_api)

    # 4. Update fetch logic in sendMessage
    old_fetch_send = """        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt }),
            });
            const data = await response.json();
            addMessage('bot', data.result || "Desculpe, tive um problema de conexão.");
        } catch(e) {
            addMessage('bot', "Erro na comunicação com a API.");
        }"""
        
    new_fetch_send = """        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt }),
            });
            if (!response.ok) {
                const errText = await response.text();
                console.error("API Error Response:", response.status, errText);
                throw new Error("HTTP error " + response.status);
            }
            const data = await response.json();
            if (data.error) {
                console.error("API Payload Error:", data.error);
                throw new Error(data.error);
            }
            addMessage('bot', data.result || "Desculpe, a IA retornou uma resposta vazia.");
        } catch(e) {
            console.error("Fetch Error:", e);
            addMessage('bot', "Desculpe, tive um problema de conexão. Detalhes no console.");
        }"""
    html = html.replace(old_fetch_send, new_fetch_send)
    
    # 5. Update fetch logic in endSimulation
    old_fetch_end = """        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: coachPrompt }),
            });
            const data = await response.json();"""
            
    new_fetch_end = """        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: coachPrompt }),
            });
            if (!response.ok) {
                const errText = await response.text();
                console.error("Coach API Error Response:", response.status, errText);
                throw new Error("HTTP error " + response.status);
            }
            const data = await response.json();
            if (data.error) {
                console.error("Coach API Payload Error:", data.error);
                throw new Error(data.error);
            }"""
    html = html.replace(old_fetch_end, new_fetch_end)

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
