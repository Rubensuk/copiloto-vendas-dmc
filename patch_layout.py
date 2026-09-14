import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change "Top 10:" label to "Sua Posição:"
    target_top10 = """<span class="text-sm text-slate-500 font-medium">Top 10:</span>"""
    inject_top10 = """<span class="text-sm text-slate-500 font-medium">Sua Posição:</span>"""
    html = html.replace(target_top10, inject_top10)

    # 1. We are going to restructure the <main id="landing-screen">.
    # Currently it starts with:
    # <main id="landing-screen" class="relative z-10 pt-20">
    #     <!-- Hero Section -->
    #     <section class="max-w-6xl mx-auto px-6 py-12 md:py-20 flex flex-col items-center md:items-start text-center md:text-left">
    
    # We will replace that with a grid wrapper
    target_main_start = """    <main id="landing-screen" class="relative z-10 pt-20">
        <!-- Hero Section -->
        <section class="max-w-6xl mx-auto px-6 py-12 md:py-20 flex flex-col items-center md:items-start text-center md:text-left">"""
        
    inject_main_start = """    <main id="landing-screen" class="relative z-10 pt-20">
        <div class="max-w-7xl mx-auto px-6 pb-20 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Coluna Esquerda -->
        <div class="lg:col-span-7 flex flex-col space-y-8">
        
        <!-- Hero Section -->
        <section class="py-12 md:py-16 flex flex-col items-center md:items-start text-center md:text-left bg-darkbg/50 rounded-3xl border border-slate-800 p-8 shadow-2xl">"""

    html = html.replace(target_main_start, inject_main_start)

    # 2. Fix the Personas section to fit in the left column
    target_personas = """        <!-- Seção: Escolha seu cliente -->
        <section class="border-t border-slate-800 bg-darkbg/50 px-6 py-10">
            <div class="max-w-6xl mx-auto">"""
    
    inject_personas = """        <!-- Seção: Escolha seu cliente -->
        <section class="bg-darkbg/50 px-6 py-8 rounded-3xl border border-slate-800 shadow-xl">
            <div class="w-full">"""
            
    html = html.replace(target_personas, inject_personas)

    # 3. Move Ranking into the Right Column
    target_ranking = """        <!-- Ranking na Tela Inicial -->
        <section class="border-t border-slate-800 bg-darkbg px-6 py-10" id="landing-ranking-section">
            <div class="max-w-4xl mx-auto">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">🏆 Pódio Global (Top 10)</h2>"""
                    
    inject_ranking = """        </div> <!-- Fim Coluna Esquerda -->
        
        <!-- Coluna Direita: Ranking na Tela Inicial -->
        <div class="lg:col-span-5 sticky top-28" id="landing-ranking-section">
            <div class="bg-cardbg rounded-3xl shadow-2xl border border-slate-700 p-6 flex flex-col max-h-[80vh]">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">🏆 Top 10 Global</h2>"""

    html = html.replace(target_ranking, inject_ranking)

    # Close the ranking divs and grid correctly
    target_ranking_end = """                <div class="bg-cardbg rounded-2xl shadow-xl border border-slate-700 p-4 md:p-6 min-h-[200px]" id="ranking-list">
                    <div class="flex justify-center items-center h-full"><span class="text-teal-400">Carregando pódio...</span></div>
                </div>
            </div>
        </section>
    </main>"""

    inject_ranking_end = """                <div class="flex-1 overflow-y-auto pr-2 hide-scroll min-h-[300px]" id="ranking-list">
                    <div class="flex justify-center items-center h-full"><span class="text-teal-400">Carregando pódio...</span></div>
                </div>
            </div>
        </div> <!-- Fim Coluna Direita -->
        </div> <!-- Fim Grid -->
    </main>"""

    html = html.replace(target_ranking_end, inject_ranking_end)
    
    # 4. Limit ranking UI to Top 10 BUT let it check rank for all
    target_slice = """                let htmlStr = '<div class="space-y-3">';
                data.forEach((item, index) => {"""
    inject_slice = """                let htmlStr = '<div class="space-y-3">';
                data.slice(0, 10).forEach((item, index) => {"""
    html = html.replace(target_slice, inject_slice)


    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
