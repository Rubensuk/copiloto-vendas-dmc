import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # ADD transformHeader TO Papa.parse
    papa_opts = """
                Papa.parse(csvText, {
                    header: true,
                    skipEmptyLines: true,
                    transformHeader: function(h) { return h ? h.trim() : h; },
    """
    html = re.sub(r"Papa\.parse\(csvText, \{\s*header: true,\s*skipEmptyLines: true,", papa_opts.strip(), html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
