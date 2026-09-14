import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject Score UI before coach-report-content
    target_report = """<div id="coach-report-content" class="hidden bg-cardbg border border-slate-800 rounded-2xl p-6 md:p-10 shadow-2xl leading-relaxed text-slate-300">"""
    
    score_injection = """
                <!-- Inject Score -->
                <div class="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 mb-8 text-center flex flex-col items-center justify-center shadow-lg">
                    <h3 class="text-lg text-slate-400 mb-4 font-medium uppercase tracking-wide">Sua Pontuação Final</h3>
                    <div class="relative w-32 h-32 flex items-center justify-center rounded-full bg-slate-900 border-4 border-slate-700 mb-6 shadow-inner transition-colors duration-1000" id="score-circle">
                        <span id="final-score" class="text-5xl font-black text-white">--</span>
                    </div>
                    <button id="btn-ver-ranking" class="px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-400 hover:to-orange-400 text-white font-bold rounded-full shadow-lg shadow-yellow-500/20 transition-all hover:-translate-y-1 flex items-center gap-2">
                        🏆 Ver Ranking Global
                    </button>
                </div>
                <!-- Fim Inject Score -->
                
                <div id="coach-report-content" class="hidden bg-cardbg border border-slate-800 rounded-2xl p-6 md:p-10 shadow-2xl leading-relaxed text-slate-300">"""
                
    if 'id="score-circle"' not in html:
        html = html.replace(target_report, score_injection)
        
    # 2. Inject Ranking Screen HTML before the closing </main> or </body>
    target_end = """    <!-- Audio elements -->"""
    
    ranking_screen = """
    <!-- Ranking Screen -->
    <main id="ranking-screen" class="hidden flex flex-col h-screen bg-darkbg max-w-4xl mx-auto p-4 md:p-8">
        <div class="text-center mb-8 mt-10">
            <h1 class="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500 tracking-tight drop-shadow-md">
                🏆 TOP 10 VENDEDORES
            </h1>
            <p class="text-slate-400 mt-2 text-lg">Os maiores negociadores da DMC</p>
        </div>

        <div class="bg-cardbg rounded-3xl shadow-2xl border border-slate-700 p-6 md:p-8 flex-1 overflow-hidden flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-white">Ranking Global</h2>
                <button id="btn-atualizar-ranking" class="text-blue-400 hover:text-blue-300 transition-colors p-2 bg-blue-900/20 rounded-full" title="Atualizar">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                </button>
            </div>
            
            <div class="overflow-y-auto flex-1 pr-2 hide-scroll" id="ranking-list">
                <!-- Preenchido via JS -->
            </div>

            <div class="mt-8 flex justify-center">
                <button onclick="location.reload()" class="px-8 py-4 bg-slate-700 hover:bg-slate-600 text-white font-bold rounded-2xl transition-colors shadow-lg">
                    🎮 Jogar Novamente
                </button>
            </div>
        </div>
    </main>

    <!-- Audio elements -->"""

    if 'id="ranking-screen"' not in html:
        html = html.replace(target_end, ranking_screen)

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
