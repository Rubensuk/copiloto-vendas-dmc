import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Start of main
    html = html.replace(
        '<main id="landing-screen" class="relative z-10 pt-20">',
        '<main id="landing-screen" class="relative z-10 pt-20 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-start px-4 lg:px-6 pb-12">\n<div class="lg:col-span-7 flex flex-col space-y-6">'
    )

    # 2. Hero Section
    html = html.replace(
        '        <section class="flex-grow flex items-center py-12 md:py-20 px-6">',
        '        <section class="flex-grow flex items-center py-10 px-6 bg-darkbg/40 rounded-3xl border border-slate-800 shadow-xl">'
    )

    # 3. Personas Section
    html = html.replace(
        '        <section class="border-t border-slate-800 bg-darkbg/50 px-6 py-10">',
        '        <section class="bg-darkbg/40 px-6 py-8 rounded-3xl border border-slate-800 shadow-xl">'
    )

    # 4. Closing the left column and opening the right column
    html = html.replace(
        '        <!-- Ranking na Tela Inicial -->\n        <section class="border-t border-slate-800 bg-darkbg px-6 py-10" id="landing-ranking-section">',
        '        </div>\n\n        <!-- Coluna Direita (Ranking Fixo) -->\n        <div class="lg:col-span-5 sticky top-28">\n        <section class="bg-cardbg rounded-3xl shadow-2xl border border-slate-700 p-6 flex flex-col max-h-[80vh]" id="landing-ranking-section">'
    )

    # 5. Fix ranking list div to scroll properly
    html = html.replace(
        '<div class="bg-cardbg rounded-2xl shadow-xl border border-slate-700 p-4 md:p-6 min-h-[200px]" id="ranking-list">',
        '<div class="flex-1 overflow-y-auto pr-2 hide-scroll min-h-[300px]" id="ranking-list">'
    )

    # 6. End of right column
    html = html.replace(
        '            </div>\n        </section>\n    </main>',
        '            </div>\n        </section>\n        </div>\n    </main>'
    )
    
    # 7. Update checkPersonalScore to show Rank Position
    target_check = """                const nota = globalRankingData[foundIndex].nota;
                scoreSpan.innerText = nota + ' pts';
                scoreSpan.className = 'text-lg font-black text-yellow-400 drop-shadow-md';"""
    inject_check = """                const nota = globalRankingData[foundIndex].nota;
                const position = foundIndex + 1;
                scoreSpan.innerHTML = nota + ' pts <span class="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded ml-2 shadow-sm">#' + position + '</span>';
                scoreSpan.className = 'text-lg font-black text-yellow-400 drop-shadow-md flex items-center';"""
    html = html.replace(target_check, inject_check)

    # 8. Limit Ranking List to Top 10 visually
    html = html.replace(
        'data.forEach((item, index) => {',
        'data.slice(0, 10).forEach((item, index) => {'
    )
    
    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
