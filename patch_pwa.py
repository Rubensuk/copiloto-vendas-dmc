import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add manifest to head
    if 'manifest.json' not in html:
        html = html.replace('<head>', '<head>\n    <link rel="manifest" href="manifest.json">')
        
    # Add SW registration at the end of scripts
    sw_script = """
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW falhou: ', err));
            });
        }
    </script>
</body>
"""
    if 'serviceWorker.register' not in html:
        html = html.replace('</body>', sw_script)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
