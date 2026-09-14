import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject Login Fields in Landing Screen
    if 'id="rn-input"' not in html:
        # Find where to inject. Before "Selecione o Cliente"
        target_html = """<h2 class="text-2xl font-bold text-white mb-6">Selecione o Cliente (Desafio)</h2>"""
        injection = """
            <div class="bg-gray-800 p-6 rounded-xl border border-gray-700 mb-8 shadow-lg">
                <h2 class="text-lg font-bold text-teal-400 mb-4">1. Seu Crachá</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm text-gray-400 mb-1">Rota (RN)</label>
                        <input type="text" id="rn-input" placeholder="Ex: 314" class="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:outline-none focus:border-teal-500">
                    </div>
                    <div>
                        <label class="block text-sm text-gray-400 mb-1">Seu Nome</label>
                        <input type="text" id="nome-input" placeholder="Ex: João Silva" class="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-white focus:outline-none focus:border-teal-500">
                    </div>
                </div>
            </div>
            
            <h2 class="text-2xl font-bold text-white mb-6">2. Selecione o Cliente (Desafio)</h2>
        """
        html = html.replace(target_html, injection)
        
    # 2. Inject Ranking Screen & Score UI
    if 'id="ranking-screen"' not in html:
        # Find coach screen end to add ranking screen
        target_end_coach = """        </div>
    </div>""" # end of coach-screen
        
        # In the coach screen, find the report div to insert the score above it
        coach_report_div = """<div id="coach-report" class="prose prose-invert prose-teal max-w-none mb-8"></div>"""
        score_injection = """
                <div class="bg-gray-800 p-6 rounded-xl border border-gray-700 mb-8 text-center flex flex-col items-center justify-center">
                    <h3 class="text-lg text-gray-400 mb-2">Sua Pontuação Final</h3>
                    <div class="relative w-32 h-32 flex items-center justify-center rounded-full bg-gray-900 border-4 border-gray-700 mb-4" id="score-circle">
                        <span id="final-score" class="text-4xl font-black text-white">--</span>
                    </div>
                    <button id="btn-ver-ranking" class="px-6 py-2 bg-gradient-to-r from-yellow-400 to-yellow-600 hover:from-yellow-500 hover:to-yellow-700 text-white font-bold rounded-full shadow-lg transition-all flex items-center gap-2">
                        🏆 Ver Ranking Global
                    </button>
                </div>
                <div id="coach-report" class="prose prose-invert prose-teal max-w-none mb-8"></div>
        """
        html = html.replace(coach_report_div, score_injection)
        
        ranking_screen = """
    <!-- Ranking Screen -->
    <div id="ranking-screen" class="hidden flex flex-col h-screen max-w-4xl mx-auto p-4 md:p-8">
        <div class="text-center mb-8">
            <h1 class="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500 tracking-tight drop-shadow-md">
                🏆 TOP 10 VENDEDORES
            </h1>
            <p class="text-gray-400 mt-2 text-lg">Os maiores negociadores da DMC</p>
        </div>

        <div class="bg-gray-800 rounded-2xl shadow-2xl border border-gray-700 p-4 md:p-8 flex-1 overflow-hidden flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-white">Ranking Global</h2>
                <button id="btn-atualizar-ranking" class="text-teal-400 hover:text-teal-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                </button>
            </div>
            
            <div class="overflow-y-auto flex-1 pr-2" id="ranking-list">
                <!-- Preenchido via JS -->
                <div class="flex justify-center items-center h-full text-gray-500">
                    <svg class="animate-spin h-8 w-8 text-teal-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </div>
            </div>

            <div class="mt-8 flex justify-center">
                <button onclick="location.reload()" class="px-8 py-4 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-xl transition-colors shadow-lg">
                    🎮 Jogar Novamente
                </button>
            </div>
        </div>
    </div>
        """
        html = html.replace('<!-- Overlay para fim de jogo -->', ranking_screen + '\n    <!-- Overlay para fim de jogo -->')

    # 3. Update Javascript Logic
    js_hook = "let selectedPersona = null;"
    if "const WEBHOOK_URL =" not in html:
        js_injection = """
        const WEBHOOK_URL = ""; // SERA SUBSTITUIDO
        let selectedPersona = null;
        let credenciais = { rn: '', nome: '' };
        """
        html = html.replace(js_hook, js_injection)
        
    # Start Chat button logic
    old_start = """
        document.querySelectorAll('.persona-card').forEach(card => {
            card.addEventListener('click', () => {
                const personaId = card.getAttribute('data-id');
                selectedPersona = personas[personaId];
                
                document.getElementById('landing-screen').classList.add('hidden');
                document.getElementById('chat-screen').classList.remove('hidden');
                document.getElementById('chat-screen').classList.add('flex');
                
                startChat();
            });
        });
    """
    new_start = """
        document.querySelectorAll('.persona-card').forEach(card => {
            card.addEventListener('click', () => {
                const rnInput = document.getElementById('rn-input').value.trim();
                const nomeInput = document.getElementById('nome-input').value.trim();
                
                if (!rnInput || !nomeInput) {
                    alert("Por favor, preencha sua Rota (RN) e seu Nome antes de selecionar o cliente!");
                    document.getElementById('rn-input').focus();
                    return;
                }
                
                credenciais.rn = rnInput;
                credenciais.nome = nomeInput;

                const personaId = card.getAttribute('data-id');
                selectedPersona = personas[personaId];
                
                document.getElementById('landing-screen').classList.add('hidden');
                document.getElementById('chat-screen').classList.remove('hidden');
                document.getElementById('chat-screen').classList.add('flex');
                
                startChat();
            });
        });
    """
    html = html.replace(old_start, new_start)

    # Inject Coach scoring requirement in system prompt
    coach_prompt_target = """Baseie sua avaliação nas regras restritas de trade (nunca ceder geladeira sem contrapartida, nunca quebrar regras de crédito, não aceitar desculpas esfarrapadas). Seja duro, direto e foque no resultado comercial.
"""
    coach_prompt_add = """
IMPORTANTE: No final absoluto da sua resposta, você DEVE gerar uma nota numérica de 0 a 100 avaliando o vendedor. Use EXATAMENTE este formato na última linha:
[NOTA: 85]
"""
    if "IMPORTANTE: No final absoluto da sua resposta" not in html:
        html = html.replace(coach_prompt_target, coach_prompt_target + coach_prompt_add)

    # Process score in endSimulation
    end_sim_target = """                const data = await response.json();
                const coachResponse = data.result || "Relatório indisponível.";"""
                
    end_sim_inject = """                const data = await response.json();
                let coachResponse = data.result || "Relatório indisponível.";
                
                // Extrair Nota
                const notaMatch = coachResponse.match(/\\[NOTA:\\s*(\\d+)\\]/i);
                const nota = notaMatch ? parseInt(notaMatch[1]) : 0;
                
                // Limpar texto
                coachResponse = coachResponse.replace(/\\[NOTA:\\s*\\d+\\]/gi, '').trim();
                
                // Animar círculo de cor da nota
                const circle = document.getElementById('score-circle');
                const scoreText = document.getElementById('final-score');
                scoreText.innerText = nota;
                
                circle.classList.remove('border-gray-700', 'border-red-500', 'border-yellow-500', 'border-teal-500');
                if(nota >= 80) circle.classList.add('border-teal-500', 'text-teal-400');
                else if(nota >= 60) circle.classList.add('border-yellow-500', 'text-yellow-400');
                else circle.classList.add('border-red-500', 'text-red-400');

                // Enviar para o Ranking (se tiver webhook configurado)
                if (WEBHOOK_URL) {
                    try {
                        fetch(WEBHOOK_URL, {
                            method: 'POST',
                            headers: {'Content-Type': 'text/plain'},
                            body: JSON.stringify({
                                nome: credenciais.nome,
                                rn: credenciais.rn,
                                persona: selectedPersona.name,
                                nota: nota
                            })
                        }).catch(e => console.log('Erro ao postar ranking', e));
                    } catch(e) {}
                }
"""
    if "// Extrair Nota" not in html:
        html = html.replace(end_sim_target, end_sim_inject)

    # Ranking logic
    ranking_logic = """
        // Ranking Logic
        const btnVerRanking = document.getElementById('btn-ver-ranking');
        const btnAtualizarRanking = document.getElementById('btn-atualizar-ranking');
        
        async function carregarRanking() {
            const listDiv = document.getElementById('ranking-list');
            listDiv.innerHTML = '<div class="flex justify-center items-center h-full"><span class="text-teal-400">Carregando pódio...</span></div>';
            
            if (!WEBHOOK_URL) {
                listDiv.innerHTML = '<div class="text-center text-red-400 mt-10">WebHook do Google Sheets não configurado!</div>';
                return;
            }
            
            try {
                const res = await fetch(WEBHOOK_URL);
                const data = await res.json();
                
                if (!data || data.length === 0) {
                    listDiv.innerHTML = '<div class="text-center text-gray-400 mt-10">Nenhuma pontuação registrada ainda. Seja o primeiro!</div>';
                    return;
                }
                
                let htmlStr = '<div class="space-y-3">';
                data.forEach((item, index) => {
                    let positionClass = "bg-gray-700 text-gray-400";
                    if (index === 0) positionClass = "bg-yellow-500 text-yellow-900 font-black shadow-lg shadow-yellow-500/20 transform scale-105";
                    else if (index === 1) positionClass = "bg-gray-300 text-gray-800 font-bold";
                    else if (index === 2) positionClass = "bg-orange-400 text-orange-900 font-bold";
                    
                    let medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}º`;
                    
                    htmlStr += `
                        <div class="${positionClass} rounded-xl p-4 flex items-center justify-between transition-all">
                            <div class="flex items-center gap-4">
                                <span class="text-2xl w-8 text-center">${medal}</span>
                                <div>
                                    <div class="text-lg uppercase tracking-wider">${item.nome}</div>
                                    <div class="text-xs opacity-75">RN ${item.rn} • Batalhou com ${item.persona}</div>
                                </div>
                            </div>
                            <div class="text-3xl font-black">${item.nota}</div>
                        </div>
                    `;
                });
                htmlStr += '</div>';
                listDiv.innerHTML = htmlStr;
            } catch(e) {
                listDiv.innerHTML = `<div class="text-center text-red-400 mt-10">Erro ao carregar ranking: ${e.message}</div>`;
            }
        }

        if (btnVerRanking) {
            btnVerRanking.addEventListener('click', () => {
                document.getElementById('coach-screen').classList.add('hidden');
                document.getElementById('coach-screen').classList.remove('flex');
                
                document.getElementById('ranking-screen').classList.remove('hidden');
                document.getElementById('ranking-screen').classList.add('flex');
                
                carregarRanking();
            });
        }
        
        if (btnAtualizarRanking) {
            btnAtualizarRanking.addEventListener('click', carregarRanking);
        }
    """
    
    if "// Ranking Logic" not in html:
        # insert right before </script>
        html = html.replace('</script>\n</body>', ranking_logic + '\n    </script>\n</body>')

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
