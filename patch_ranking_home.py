import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject Ranking into Landing Screen
    target_end_landing = """        </section>
    </main>


    <!-- TELA 2: CHAT DA SIMULAÇÃO -->"""
    
    inject_landing = """        </section>
        
        <!-- Ranking na Tela Inicial -->
        <section class="border-t border-slate-800 bg-darkbg px-6 py-10" id="landing-ranking-section">
            <div class="max-w-4xl mx-auto">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">🏆 Pódio Global (Top 10)</h2>
                    <button id="btn-atualizar-ranking" class="text-slate-400 hover:text-white transition-colors" title="Atualizar Ranking">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                    </button>
                </div>
                <div class="bg-cardbg rounded-2xl shadow-xl border border-slate-700 p-4 md:p-6 min-h-[200px]" id="ranking-list">
                    <div class="flex justify-center items-center h-full"><span class="text-teal-400">Carregando pódio...</span></div>
                </div>
            </div>
        </section>
    </main>


    <!-- TELA 2: CHAT DA SIMULAÇÃO -->"""

    if 'id="landing-ranking-section"' not in html:
        html = html.replace(target_end_landing, inject_landing)


    # 2. Update JavaScript to call carregarRanking() on init
    target_init = """        function initApp() {
            renderPersonas();
            selectPersona(PERSONAS[0].id);
        }"""
        
    inject_init = """        function initApp() {
            renderPersonas();
            selectPersona(PERSONAS[0].id);
            carregarRanking();
        }"""
        
    if "carregarRanking();\n        }" not in html:
        html = html.replace(target_init, inject_init)


    # 3. Modify btnVerRanking logic to go back to Landing
    target_btn = """        if (btnVerRanking) {
            btnVerRanking.addEventListener('click', () => {
                document.getElementById('coach-screen').classList.add('hidden');
                document.getElementById('coach-screen').classList.remove('flex');
                
                document.getElementById('ranking-screen').classList.remove('hidden');
                document.getElementById('ranking-screen').classList.add('flex');
                
                carregarRanking();
            });
        }"""
        
    inject_btn = """        if (btnVerRanking) {
            btnVerRanking.addEventListener('click', () => {
                document.getElementById('coach-screen').classList.add('hidden');
                document.getElementById('landing-screen').classList.remove('hidden');
                document.getElementById('main-header').classList.remove('-translate-y-full'); // Volta header
                
                carregarRanking();
                
                // Scroll para o ranking
                setTimeout(() => {
                    const rankingSection = document.getElementById('landing-ranking-section');
                    if(rankingSection) rankingSection.scrollIntoView({ behavior: 'smooth' });
                }, 100);
            });
        }"""
        
    if "document.getElementById('landing-screen').classList.remove('hidden');" not in html:
        html = html.replace(target_btn, inject_btn)
        
    # 4. Remove the old ranking-screen HTML and old button listener if needed
    # Actually, the old ranking-screen has `<div id="ranking-list">`. We need to remove it so there are no duplicate IDs!
    # Because if there are two `ranking-list` IDs, document.getElementById('ranking-list') will grab the wrong one!
    
    # Let's completely nuke the old ranking-screen
    start_str = "    <!-- Ranking Screen -->"
    end_str = "    <!-- Audio elements -->"
    
    if start_str in html and end_str in html:
        before = html.split(start_str)[0]
        after = html.split(end_str)[1]
        html = before + end_str + after

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
