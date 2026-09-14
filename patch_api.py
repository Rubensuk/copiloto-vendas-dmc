import re

def patch():
    with open('api/sheet.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # Add Cache-Control header right after Content-Type
    old_header = "res.setHeader('Content-Type', 'text/csv');"
    new_header = "res.setHeader('Content-Type', 'text/csv');\n        res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=60');"
    
    if 'Cache-Control' not in code:
        code = code.replace(old_header, new_header)

    with open('api/sheet.js', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    patch()
