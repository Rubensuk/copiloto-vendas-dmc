def patch():
    with open('simulador.html', 'r', encoding='utf-8') as f:
        html = f.read()

    inject = '''    <script>
        const WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbx6YRvO3mDePSXevXF_UNnX5NWlXmR3QJx-iNd2jEYULXDkkgV044tjv7OlciGKNcs/exec";
        let credenciais = { rn: "", nome: "" };
        const PERSONAS'''
        
    html = html.replace('    <script>\n        const PERSONAS', inject)
    
    with open('simulador.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
