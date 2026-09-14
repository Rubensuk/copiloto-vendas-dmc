import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update HE_600 mapping
    old_he_600 = r"const HE_600 = \{'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'BUD 600': 'Budweiser 600ml', 'COR 600': 'Corona 600ml', 'ORI 600 ': 'Original 600ml', 'OUTROS 600': 'Outros 600ml'\};"
    new_he_600 = "const HE_600 = {'SPT 600': 'Spaten 600ml', 'SPT 601': 'Stella Artois 600ml', 'SPT 602': 'Stella Puro Glúten 600ml', 'SPT 603': 'Budweiser 600ml', 'SPT 604': 'Corona 600ml', 'SPT 605': 'Original 600ml', 'SPT 606': 'Outros 600ml'};"
    html = re.sub(old_he_600, new_he_600, html)

    # 2. Update HE_LN mapping
    old_he_ln = r"const HE_LN = \{'COR LN': 'Corona Long Neck', 'STL LN': 'Stella Artois Long Neck', 'STL PG LN': 'Stella Puro Glúten Long Neck', 'SPT LN': 'Spaten Long Neck', 'MIC LN': 'Michelob Ultra Long Neck', 'OUTROS LN': 'Outros Long Neck', 'BUD LN': 'Budweiser Long Neck'\};"
    new_he_ln = "const HE_LN = {'SPT 607': 'Corona Long Neck', 'SPT 608': 'Stella Artois Long Neck', 'SPT 609': 'Stella Puro Glúten Long Neck', 'SPT 610': 'Spaten Long Neck', 'SPT 611': 'Michelob Ultra Long Neck', 'SPT 612': 'Outros Long Neck', 'SPT 613': 'Budweiser Long Neck'};"
    html = re.sub(old_he_ln, new_he_ln, html)

    # 3. Update CORE_600 mapping
    old_core_600 = r"const CORE_600 = \{'AP 600': 'Antarctica 600ml', 'BC 600': 'Brahma 600ml', 'BUD 600 ': 'Budweiser 600ml', 'ORI 600': 'Original 600ml', 'SK 600': 'Skol 600ml', 'SPT 600 ': 'Spaten 600ml', 'STL 600 ': 'Stella Artois 600ml', 'STL PG 600 ': 'Stella Puro Glúten 600ml', ' OUTROS 600 ': 'Outros 600ml'\};"
    new_core_600 = "const CORE_600 = {'SPT 617': 'Antarctica 600ml', 'SPT 618': 'Brahma 600ml', 'SPT 619': 'Budweiser 600ml', 'SPT 620': 'Original 600ml', 'SPT 621': 'Skol 600ml', 'SPT 622': 'Spaten 600ml', 'SPT 623': 'Stella Artois 600ml', 'SPT 624': 'Stella Puro Glúten 600ml', ' OUTROS 600 ': 'Outros 600ml'};"
    html = re.sub(old_core_600, new_core_600, html)

    # 4. Remove 1000ml from rendering
    # Find the line: for (let col in CORE_1000) { ... }
    # and remove it.
    old_loop = r"for \(let col in CORE_1000\) \{ if \(row\[col\] !== undefined && row\[col\] !== ''\) mix_items \+= formatRow\(gerarQuadrado\(safeInt\(row\[col\]\) > 0\), CORE_1000\[col\], safeInt\(row\[col\]\)\); \}"
    html = re.sub(old_loop, "", html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
