import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    correct_mappings = """
                const HE_600 = {'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'BUD 600': 'Budweiser 600ml', 'COR 600': 'Corona 600ml', 'ORI 600': 'Original 600ml', 'OUTROS 600': 'Outros 600ml'};
                const HE_LN = {'COR LN': 'Corona Long Neck', 'STL LN': 'Stella Artois Long Neck', 'STL PG LN': 'Stella Puro Glúten Long Neck', 'SPT LN': 'Spaten Long Neck', 'MIC LN': 'Michelob Ultra Long Neck', 'OUTROS LN': 'Outros Long Neck', 'BUD LN': 'Budweiser Long Neck'};
                const CORE_600 = {'AP 600': 'Antarctica 600ml', 'BC 600': 'Brahma 600ml', 'BUD 600': 'Budweiser 600ml', 'ORI 600': 'Original 600ml', 'SK 600': 'Skol 600ml', 'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'OUTROS 600': 'Outros 600ml'};
                const CORE_300 = {'AP 300': 'Antarctica 300ml', 'BC 300': 'Brahma 300ml', 'BUD 300': 'Budweiser 300ml', 'ORI 300': 'Original 300ml', 'SK 300': 'Skol 300ml', 'OUTROS 300': 'Outros 300ml'};
                const CORE_1000 = {'AP 1000': 'Antarctica 1000ml', 'BC 1000': 'Brahma 1000ml', 'BUD 1000': 'Budweiser 1000ml', 'ORI 1000': 'Original 1000ml', 'SK 1000': 'Skol 1000ml', 'OUTROS 1000': 'Outros 1000ml'};
    """

    old_pattern = r"const HE_600 = \{'ORIGINAL': 'Original 600ml'.*?const CORE_1000 = \{'BRAHMA_1000': 'Brahma Litrão', 'SKOL_1000': 'Skol Litrão'\};"

    html = re.sub(old_pattern, correct_mappings.strip(), html, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
