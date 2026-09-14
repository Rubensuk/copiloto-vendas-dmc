import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The buggy line:
    # const categoria = document.getElementById('category-select').value;
    
    old_code = "const categoria = document.getElementById('category-select').value;"
    new_code = "const prodSelect = document.getElementById('product-select');\n            const categoria = prodSelect.options[prodSelect.selectedIndex].getAttribute('data-category') || 'Bebidas';"
    
    html = html.replace(old_code, new_code)
    
    # Also I should wrap getRawPrompt in the try block or just leave it since it won't crash now.
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
