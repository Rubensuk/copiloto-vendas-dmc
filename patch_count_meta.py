import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The current line counting bateu meta
    old_count = """                    if (safeInt(row['BATEU META']) === 1) agg.count_bateu_meta = (agg.count_bateu_meta || 0) + 1;"""

    # We need to remove it from the top of the loop, and put it AFTER total_pct is calculated.
    # Where is it right now?
    html = html.replace(old_count, "")

    # Now let's find the new insertion point.
    target = """                    if (bateu === 1 || total_pct >= 100) {
                        status_txt = "<span style='color:#22c55e;'>✅ BATEU META</span>";
                    } else if (total_pct > 50) {"""
    
    replacement = """                    if (bateu === 1 || total_pct >= 100) {
                        status_txt = "<span style='color:#22c55e;'>✅ BATEU META</span>";
                        agg.count_bateu_meta = (agg.count_bateu_meta || 0) + 1;
                    } else if (total_pct > 50) {"""

    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
