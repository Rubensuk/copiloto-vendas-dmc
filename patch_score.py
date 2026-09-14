import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Coach Prompt to ask for score
    old_prompt = """(roteiros literais do que dizer para melhorar)`;"""
    new_prompt = """(roteiros literais do que dizer para melhorar)

IMPORTANTE: No final absoluto da sua resposta, você DEVE gerar uma nota numérica de 0 a 100 avaliando o vendedor. Use EXATAMENTE este formato na última linha:
[NOTA: 85]`;"""
    
    html = html.replace(old_prompt, new_prompt)

    # 2. Extract score and push to Google Webhook
    old_fetch_logic = """const data = await response.json();
                
                document.getElementById('coach-loading').classList.add('hidden');"""
                
    new_fetch_logic = """const data = await response.json();
                
                let rawResult = data.result || "Erro ao processar.";
                
                // Extrair Nota
                const notaMatch = rawResult.match(/\\[NOTA:\\s*(\\d+)\\]/i);
                const nota = notaMatch ? parseInt(notaMatch[1]) : 0;
                rawResult = rawResult.replace(/\\[NOTA:\\s*\\d+\\]/gi, '').trim();
                data.result = rawResult;
                
                // Animar círculo de cor da nota
                try {
                    const circle = document.getElementById('score-circle');
                    const scoreText = document.getElementById('final-score');
                    scoreText.innerText = nota;
                    
                    circle.classList.remove('border-gray-700', 'border-red-500', 'border-yellow-500', 'border-teal-500');
                    if(nota >= 80) circle.classList.add('border-teal-500', 'text-teal-400');
                    else if(nota >= 60) circle.classList.add('border-yellow-500', 'text-yellow-400');
                    else circle.classList.add('border-red-500', 'text-red-400');
                } catch(e) {}

                // Enviar para o Ranking (se tiver webhook configurado)
                if (typeof WEBHOOK_URL !== 'undefined' && WEBHOOK_URL && typeof credenciais !== 'undefined') {
                    try {
                        fetch(WEBHOOK_URL, {
                            method: 'POST',
                            headers: {'Content-Type': 'text/plain'},
                            body: JSON.stringify({
                                nome: credenciais.nome,
                                rn: credenciais.rn,
                                persona: currentPersona.name,
                                nota: nota
                            })
                        }).catch(e => console.log('Erro post ranking', e));
                    } catch(e) {}
                }
                
                document.getElementById('coach-loading').classList.add('hidden');"""

    html = html.replace(old_fetch_logic, new_fetch_logic)

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
