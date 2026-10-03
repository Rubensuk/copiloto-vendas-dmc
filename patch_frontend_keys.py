import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    new_dicts = """const HE_600 = {'HE_SPT 600': 'Spaten 600ml', 'HE_STL 600': 'Stella Artois 600ml', 'HE_STL PG 600': 'Stella Puro Gold 600ml', 'HE_BUD 600': 'Budweiser 600ml', 'HE_COR 600': 'Corona 600ml', 'HE_ORI 600': 'Original 600ml', 'HE_OUTROS 600': 'Outros 600ml'};
                const HE_LN = {'HE_COR LN': 'Corona LN', 'HE_STL LN': 'Stella Artois LN', 'HE_STL PG LN': 'Stella Puro Gold LN', 'HE_SPT LN': 'Spaten LN', 'HE_MIC LN': 'Michelob Ultra LN', 'HE_OUTROS LN': 'Outros LN', 'HE_BUD LN': 'Budweiser LN', 'HE_BUD LN ZERO': 'Budweiser Zero LN', 'HE_COR LN ZERO': 'Corona Zero LN', 'HE_OUTROS LN ZERO': 'Outros Zero LN'};
                const CORE_600 = {'CORE_AP 600': 'Antarctica 600ml', 'CORE_BC 600': 'Brahma 600ml', 'CORE_BUD 600': 'Budweiser 600ml', 'CORE_ORI 600': 'Original 600ml', 'CORE_SK 600': 'Skol 600ml', 'CORE_SPT 600': 'Spaten 600ml', 'CORE_STL 600': 'Stella Artois 600ml', 'CORE_STL PG 600': 'Stella Puro Gold 600ml', 'CORE_OUTROS 600': 'Outros 600ml'};
                const CORE_300 = {'CORE_AP 300': 'Antarctica 300ml', 'CORE_BC 300': 'Brahma 300ml', 'CORE_BUD 300': 'Budweiser 300ml', 'CORE_ORI 300': 'Original 300ml', 'CORE_SK 300': 'Skol 300ml', 'CORE_OUTROS 300': 'Outros 300ml'};
                const CORE_1000 = {'CORE_AP 1000': 'Antarctica 1000ml', 'CORE_BC 1000': 'Brahma 1000ml', 'CORE_BUD 1000': 'Budweiser 1000ml', 'CORE_ORI 1000': 'Original 1000ml', 'CORE_SK 1000': 'Skol 1000ml', 'CORE_OUTROS 1000': 'Outros 1000ml'};"""

    pattern = re.compile(
        r'const HE_600 = \{.*?\};\s*'
        r'const HE_LN = \{.*?\};\s*'
        r'const CORE_600 = \{.*?\};\s*'
        r'const CORE_300 = \{.*?\};\s*'
        r'const CORE_1000 = \{.*?\};',
        re.DOTALL
    )
    
    html = pattern.sub(new_dicts, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
