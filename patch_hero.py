import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject UI in Hero
    # Right above the <button onclick="startChallenge()">
    target_btn = """<button onclick="startChallenge()" class="group relative px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white text-lg font-bold rounded-2xl shadow-lg shadow-blue-600/30 transition-all hover:-translate-y-1 overflow-hidden">"""
    
    inject_ui = """
                    <!-- Inject Cracha -->
                    <div class="bg-cardbg p-6 rounded-2xl border border-slate-700 mb-8 w-full max-w-xl mx-auto md:mx-0 text-left shadow-xl">
                        <h4 class="text-teal-400 font-bold mb-4 flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"></path></svg>
                            Sua Credencial (Para o Ranking)
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm text-slate-400 mb-1">Rota (RN)</label>
                                <input type="number" id="rn-input" placeholder="Ex: 314" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            </div>
                            <div>
                                <label class="block text-sm text-slate-400 mb-1">Seu Nome</label>
                                <input type="text" id="nome-input" placeholder="Ex: João" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500 transition-colors">
                            </div>
                        </div>
                    </div>
                    <!-- Fim Inject -->
                    
                    """
    
    if 'id="rn-input"' not in html:
        html = html.replace(target_btn, inject_ui + target_btn)

    # 2. Add validation in startChallenge()
    target_start = """        function startChallenge() {"""
    inject_start = """        function startChallenge() {
            const rn = document.getElementById('rn-input').value.trim();
            const nome = document.getElementById('nome-input').value.trim();
            if (!rn || !nome) {
                alert("Por favor, preencha sua Rota (RN) e seu Nome para entrar no Ranking!");
                document.getElementById('rn-input').focus();
                return;
            }
            credenciais.rn = rn;
            credenciais.nome = nome;
"""
    if "credenciais.rn = rn;" not in html:
        html = html.replace(target_start, inject_start)

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
