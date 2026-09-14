import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. ADD THEME TOGGLE BUTTON
    theme_btn = '''
        <button id="btn-theme-toggle" type="button" class="btn-limpar-campos" title="Alternar Tema Claro/Escuro" style="margin-right: 10px;">
            <span id="theme-icon">🌙</span>
            <span id="theme-text">Escuro</span>
        </button>
        <button id="btn-limpar-campos"
    '''
    html = re.sub(r'<button id="btn-limpar-campos"', theme_btn.strip(), html)
    
    # 2. ADD CSS FOR LIGHT MODE
    light_css = '''
    <style>
        body.light-mode {
            background-color: #f0f2f6;
            color: #111827;
            --text-primary: #111827;
            --text-secondary: #4b5563;
        }
        body.light-mode header {
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        body.light-mode .calculator-card, body.light-mode .output-card {
            background: #ffffff;
            border-color: #e5e7eb;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        body.light-mode .logo-text h1 {
            background: linear-gradient(to right, #111827, #4b5563);
            -webkit-background-clip: text;
        }
        body.light-mode input, body.light-mode select, body.light-mode textarea {
            background: #f9fafb;
            color: #111827;
            border-color: #d1d5db;
        }
        body.light-mode .btn-limpar-campos {
            background: #f3f4f6;
            color: #374151;
            border-color: #d1d5db;
        }
        body.light-mode .pdv-row {
            background: #f9fafb;
            border-color: #e5e7eb;
            color: #111827;
        }
        body.light-mode .pdv-details {
            border-top-color: #e5e7eb;
        }
        
        .pdv-row {
            background: rgba(255,255,255,0.03); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 8px; 
            margin-bottom: 8px; 
            font-family: var(--font-body);
        }
        .pdv-summary {
            padding: 12px 15px; 
            cursor: pointer; 
            display: flex; 
            align-items: center; 
            list-style: none;
        }
        .pdv-summary::-webkit-details-marker { display: none; }
        .pdv-details {
            padding: 15px; 
            border-top: 1px solid rgba(255,255,255,0.05);
        }
    </style>
    '''
    html = html.replace('</head>', light_css + '\n</head>')
    
    # 3. ADD JS FOR THEME TOGGLE
    theme_js = '''
        document.getElementById('btn-theme-toggle')?.addEventListener('click', function() {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            document.getElementById('theme-icon').innerText = isLight ? '☀️' : '🌙';
            document.getElementById('theme-text').innerText = isLight ? 'Claro' : 'Escuro';
        });
    '''
    html = html.replace("// 1. Força a seleção", theme_js + "\n                // 1. Força a seleção")

    with open('index_patched.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
