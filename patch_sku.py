import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Define the new correct dictionaries based exactly on the CSV headers
    new_dicts = """const HE_600 = {'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'BUD 600': 'Budweiser 600ml', 'COR 600': 'Corona 600ml', 'ORI 600 ': 'Original 600ml', 'OUTROS 600': 'Outros 600ml'};
                const HE_LN = {'COR LN': 'Corona LN', 'STL LN': 'Stella Artois LN', 'STL PG LN': 'Stella Puro Glúten LN', 'SPT LN': 'Spaten LN', 'MIC LN': 'Michelob Ultra LN', 'OUTROS LN': 'Outros LN', 'BUD LN': 'Budweiser LN', 'BUD LN ZERO': 'Budweiser Zero LN', 'COR LN ZERO': 'Corona Zero LN', 'OUTROS LN ZERO': 'Outros Zero LN'};
                const CORE_600 = {'AP 600': 'Antarctica 600ml', 'BC 600': 'Brahma 600ml', 'BUD 600 ': 'Budweiser 600ml', 'ORI 600': 'Original 600ml', 'SK 600': 'Skol 600ml', 'SPT 600 ': 'Spaten 600ml', 'STL 600 ': 'Stella Artois 600ml', 'STL PG 600 ': 'Stella Puro Glúten 600ml', ' OUTROS 600 ': 'Outros 600ml'};
                const CORE_300 = {'AP 300': 'Antarctica 300ml', 'BC 300': 'Brahma 300ml', 'BUD 300': 'Budweiser 300ml', 'ORI 300': 'Original 300ml', 'SK 300': 'Skol 300ml', 'OUTROS 300': 'Outros 300ml'};
                const CORE_1000 = {'AP 1000': 'Antarctica 1000ml', 'BC 1000': 'Brahma 1000ml', 'BUD 1000': 'Budweiser 1000ml', 'ORI 1000': 'Original 1000ml', 'SK 1000': 'Skol 1000ml', 'OUTROS 1000': 'Outros 1000ml'};"""

    # We need to replace the old block with this new block
    # Regex to find the block from const HE_600 to const CORE_1000
    
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
