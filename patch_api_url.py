import re

def patch():
    # Patch simulador.html
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the API_URL logic in simulador.html
    old_api_logic = """let API_URL = '/api/generate';
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.protocol === "file:") {
            API_URL = "https://dmc-copilot.vercel.app/api/generate";
        }"""
    
    new_api_logic = "const API_URL = 'https://copiloto-vendas-omega.vercel.app/api/generate';"
    
    if old_api_logic in html:
        html = html.replace(old_api_logic, new_api_logic)
    else:
        # If it doesn't match exactly, fallback to regex
        html = re.sub(
            r"let API_URL = '/api/generate';\s*if\s*\(.*?\)\s*\{\s*API_URL\s*=\s*.*?;\s*\}",
            new_api_logic,
            html,
            flags=re.DOTALL
        )

    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)


    # Patch index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()

    # Find the endpoint logic in index.html
    old_index_api = """let endpoint = "/api/generate";
                    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
                        endpoint = "https://copiloto-vendas-omega.vercel.app/api/generate";
                    }"""
    new_index_api = 'const endpoint = "https://copiloto-vendas-omega.vercel.app/api/generate";'
    
    if old_index_api in index_html:
        index_html = index_html.replace(old_index_api, new_index_api)
    else:
        index_html = re.sub(
            r"let endpoint = \"/api/generate\";\s*if\s*\(.*?\)\s*\{\s*endpoint\s*=\s*.*?;\s*\}",
            new_index_api,
            index_html,
            flags=re.DOTALL
        )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

if __name__ == '__main__':
    patch()
