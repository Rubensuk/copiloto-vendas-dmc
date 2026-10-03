import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The old condition
    old_logic = "let cor = pct < 40 ? '#ef4444' : (pct < 75 ? '#f59e0b' : '#22c55e');"
    
    # The new condition
    new_logic = "let cor = pct <= 50 ? '#ef4444' : (pct < 100 ? '#f59e0b' : '#22c55e');"

    # Replace globally in index.html (there should be exactly two occurrences)
    html = html.replace(old_logic, new_logic)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
