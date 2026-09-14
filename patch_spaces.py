import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove transformHeader from Papa.parse
    old_papa = r"transformHeader: function\(h\) \{ return h \? h\.trim\(\) : h; \},"
    html = re.sub(old_papa, "", html)

    # 2. Restore exact mappings (WITH spaces) for High End and Core
    old_mappings = r"const HE_600 = \{'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'BUD 600': 'Budweiser 600ml', 'COR 600': 'Corona 600ml', 'ORI 600': 'Original 600ml', 'OUTROS 600': 'Outros 600ml'\};\s*const HE_LN = \{'COR LN': 'Corona Long Neck', 'STL LN': 'Stella Artois Long Neck', 'STL PG LN': 'Stella Puro Glúten Long Neck', 'SPT LN': 'Spaten Long Neck', 'MIC LN': 'Michelob Ultra Long Neck', 'OUTROS LN': 'Outros Long Neck', 'BUD LN': 'Budweiser Long Neck'\};\s*const CORE_600 = \{'AP 600': 'Antarctica 600ml', 'BC 600': 'Brahma 600ml', 'BUD 600': 'Budweiser 600ml', 'ORI 600': 'Original 600ml', 'SK 600': 'Skol 600ml', 'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'OUTROS 600': 'Outros 600ml'\};"
    
    new_mappings = """const HE_600 = {'SPT 600': 'Spaten 600ml', 'STL 600': 'Stella Artois 600ml', 'STL PG 600': 'Stella Puro Glúten 600ml', 'BUD 600': 'Budweiser 600ml', 'COR 600': 'Corona 600ml', 'ORI 600 ': 'Original 600ml', 'OUTROS 600': 'Outros 600ml'};
                const HE_LN = {'COR LN': 'Corona Long Neck', 'STL LN': 'Stella Artois Long Neck', 'STL PG LN': 'Stella Puro Glúten Long Neck', 'SPT LN': 'Spaten Long Neck', 'MIC LN': 'Michelob Ultra Long Neck', 'OUTROS LN': 'Outros Long Neck', 'BUD LN': 'Budweiser Long Neck'};
                const CORE_600 = {'AP 600': 'Antarctica 600ml', 'BC 600': 'Brahma 600ml', 'BUD 600 ': 'Budweiser 600ml', 'ORI 600': 'Original 600ml', 'SK 600': 'Skol 600ml', 'SPT 600 ': 'Spaten 600ml', 'STL 600 ': 'Stella Artois 600ml', 'STL PG 600 ': 'Stella Puro Glúten 600ml', ' OUTROS 600 ': 'Outros 600ml'};"""
    
    html = re.sub(old_mappings, new_mappings, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
