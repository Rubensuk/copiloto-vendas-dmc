import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add CSS for header-actions
    css_to_add = """
        .header-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        @media (max-width: 768px) {
            header {
                flex-direction: column;
                padding: 1rem;
                gap: 1rem;
            }
            .header-actions {
                flex-direction: column;
                width: 100%;
                gap: 8px;
            }
            .header-actions > * {
                width: 100%;
                justify-content: center;
                margin-right: 0 !important;
            }
            main {
                margin: 1rem auto;
                padding: 0 1rem;
            }
        }
    </style>"""
    
    html = html.replace('</style>', css_to_add)

    # 2. Wrap the buttons in header-actions div
    # Find everything between <div class="logo-container">...</div> and <script>
    
    header_regex = re.compile(
        r'(<div class="logo-container">.*?</div>\s*)'
        r'(<a href="simulador\.html".*?</a>\s*)'
        r'(<button id="btn-theme-toggle".*?</button>\s*)'
        r'(<button id="btn-limpar-campos".*?</button>\s*)'
        r'(<script>)', re.DOTALL)
    
    def replacer(match):
        logo = match.group(1)
        treinamento = match.group(2)
        tema = match.group(3)
        limpar = match.group(4)
        script = match.group(5)
        
        return f'{logo}<div class="header-actions">\n{treinamento}{tema}{limpar}</div>\n{script}'

    html = header_regex.sub(replacer, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
