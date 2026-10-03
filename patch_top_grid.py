import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS
    html = html.replace('.score5-top-grid { grid-template-columns: repeat(4, 1fr); }', '.score5-top-grid { grid-template-columns: repeat(2, 1fr); }')

    # 2. Remove HTML for Long Neck and 300ml in the top grid
    # Target:
    target = """                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">🍾 Long Neck</div>
                        <div id="agg-ln-text" style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0/0 cxs</div>
                        <div id="agg-ln-bar" style="margin-top: 5px;"></div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 10px;">
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">🥃 300ml</div>
                        <div id="agg-300-text" style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 0.1rem;">0/0 cxs</div>
                        <div id="agg-300-bar" style="margin-top: 5px;"></div>
                    </div>"""
    
    html = html.replace(target, "")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
