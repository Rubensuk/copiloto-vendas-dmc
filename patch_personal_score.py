import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the Credencial UI to have 3 columns and include the Personal Score display
    target_credencial = """                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm text-slate-400 mb-1">Rota (RN)</label>
                                <input type="number" id="rn-input" placeholder="Ex: 314" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            </div>
                            <div>
                                <label class="block text-sm text-slate-400 mb-1">Seu Nome</label>
                                <input type="text" id="nome-input" placeholder="Ex: João" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            </div>
                        </div>"""

    inject_credencial = """                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label class="block text-sm text-slate-400 mb-1">Rota (RN)</label>
                                <input type="number" id="rn-input" placeholder="Ex: 000" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            </div>
                            <div>
                                <label class="block text-sm text-slate-400 mb-1">Seu Nome</label>
                                <input type="text" id="nome-input" placeholder="Ex: João" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            </div>
                            <div class="flex flex-col justify-end">
                                <label class="block text-sm text-slate-400 mb-1">Seu Recorde Pessoal</label>
                                <div class="bg-slate-900 border border-slate-700 rounded-xl p-3 flex items-center justify-between h-[50px]">
                                    <span class="text-sm text-slate-500 font-medium">Top 10:</span>
                                    <span id="personal-score" class="text-lg font-bold text-slate-600">Zerado</span>
                                </div>
                            </div>
                        </div>"""

    html = html.replace(target_credencial, inject_credencial)

    # 2. Inject global logic to track ranking data and personal score
    target_globals = """        const WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbx6YRvO3mDePSXevXF_UNnX5NWlXmR3QJx-iNd2jEYULXDkkgV044tjv7OlciGKNcs/exec";"""
    inject_globals = """        const WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbx6YRvO3mDePSXevXF_UNnX5NWlXmR3QJx-iNd2jEYULXDkkgV044tjv7OlciGKNcs/exec";
        let globalRankingData = [];"""
    if "let globalRankingData = [];" not in html:
        html = html.replace(target_globals, inject_globals)

    # 3. Update carregarRanking() to save globalRankingData and trigger score check
    target_fetch = """                const res = await fetch(WEBHOOK_URL);
                const data = await res.json();
                
                if (!data || data.length === 0) {"""
    inject_fetch = """                const res = await fetch(WEBHOOK_URL);
                const data = await res.json();
                
                globalRankingData = data || [];
                checkPersonalScore(); // Atualiza a caixinha do RN
                
                if (!data || data.length === 0) {"""
    if "globalRankingData = data || [];" not in html:
        html = html.replace(target_fetch, inject_fetch)

    # 4. Inject JS checkPersonalScore logic at the end of the script
    target_script_end = """    </script>
</body>"""
    inject_script_end = """
        function checkPersonalScore() {
            const rnInput = document.getElementById('rn-input');
            const scoreSpan = document.getElementById('personal-score');
            if (!rnInput || !scoreSpan) return;
            
            const rn = rnInput.value.trim();
            if (!rn) {
                scoreSpan.innerText = 'Zerado';
                scoreSpan.className = 'text-lg font-bold text-slate-600';
                return;
            }

            const foundIndex = globalRankingData.findIndex(item => item.rn == rn);
            if (foundIndex !== -1) {
                const nota = globalRankingData[foundIndex].nota;
                scoreSpan.innerText = nota + ' pts';
                scoreSpan.className = 'text-lg font-black text-yellow-400 drop-shadow-md';
            } else {
                scoreSpan.innerText = 'Zerado';
                scoreSpan.className = 'text-lg font-bold text-slate-500';
            }
        }

        // Attach listeners when DOM is ready
        setTimeout(() => {
            const rnInput = document.getElementById('rn-input');
            const nomeInput = document.getElementById('nome-input');
            if (rnInput) {
                rnInput.addEventListener('input', checkPersonalScore);
                rnInput.value = localStorage.getItem('dmc_rn') || '';
            }
            if (nomeInput) {
                nomeInput.value = localStorage.getItem('dmc_nome') || '';
            }
            checkPersonalScore();
        }, 500);
    </script>
</body>"""
    if "function checkPersonalScore()" not in html:
        html = html.replace(target_script_end, inject_script_end)

    # 5. Save credentials to localStorage on startChallenge
    target_start = """            credenciais.rn = rn;
            credenciais.nome = nome;"""
    inject_start = """            credenciais.rn = rn;
            credenciais.nome = nome;
            localStorage.setItem('dmc_rn', rn);
            localStorage.setItem('dmc_nome', nome);"""
    if "localStorage.setItem('dmc_rn'" not in html:
        html = html.replace(target_start, inject_start)

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
