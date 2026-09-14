import re

def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the checkPersonalScore function
    target_check = """                const nota = globalRankingData[foundIndex].nota;
                scoreSpan.innerText = nota + ' pts';
                scoreSpan.className = 'text-lg font-black text-yellow-400 drop-shadow-md';"""
    
    inject_check = """                const nota = globalRankingData[foundIndex].nota;
                const position = foundIndex + 1; // Rank number
                scoreSpan.innerHTML = nota + ' pts <span class="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded ml-2 shadow-sm">#' + position + '</span>';
                scoreSpan.className = 'text-lg font-black text-yellow-400 drop-shadow-md flex items-center';"""
    
    if "const position = foundIndex + 1;" not in html:
        html = html.replace(target_check, inject_check)

    # 2. Limit the ranking render to top 10
    if "data.slice(0, 10).forEach" not in html:
        html = html.replace("data.forEach((item, index) => {", "data.slice(0, 10).forEach((item, index) => {")

    # 3. Change "Top 10:" to "Sua Posição:"
    html = html.replace('<span class="text-sm text-slate-500 font-medium">Top 10:</span>', '<span class="text-sm text-slate-500 font-medium">Sua Posição:</span>')

    # 4. FIX THE CSS LAYOUT to make Ranking sticky
    
    # We replace <main id="landing-screen"...>
    html = re.sub(
        r'<main id="landing-screen" class="[^"]+">',
        '<main id="landing-screen" class="pt-16 min-h-screen max-w-[1400px] mx-auto px-4 md:px-8 grid grid-cols-1 xl:grid-cols-12 gap-8 pb-12 items-start">\n<div class="xl:col-span-8 flex flex-col space-y-6">',
        html
    )

    # Remove the <section> around the ranking
    html = html.replace(
        '        <!-- Ranking na Tela Inicial -->\n        <section class="border-t border-slate-800 bg-darkbg px-6 py-10" id="landing-ranking-section">',
        '        </div>\n        <!-- Direita: Ranking -->\n        <div class="xl:col-span-4 sticky top-24" id="landing-ranking-section">\n        <div class="bg-cardbg rounded-3xl shadow-2xl border border-slate-700 p-6 flex flex-col max-h-[85vh]">'
    )

    # Fix the inner ranking div
    html = html.replace(
        '<div class="bg-cardbg rounded-2xl shadow-xl border border-slate-700 p-4 md:p-6 min-h-[200px]" id="ranking-list">',
        '<div class="flex-1 overflow-y-auto pr-2 hide-scroll min-h-[300px]" id="ranking-list">'
    )

    # Fix the end tags
    html = html.replace(
        '            </div>\n        </section>\n    </main>',
        '            </div>\n        </div>\n    </main>'
    )
    
    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
