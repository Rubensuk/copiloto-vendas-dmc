import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target_details = """<div class="pdv-details" style="padding: 15px; border-top: 1px solid ${border_color}; color: ${text_color};">"""
    replacement_details = """<div class="pdv-details" style="padding: 15px; padding-bottom: 30px; border-top: 1px solid ${border_color}; color: ${text_color};">"""
    
    html = html.replace(target_details, replacement_details)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
