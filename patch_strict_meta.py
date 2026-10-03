import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target = """                    if (bateu === 1 || total_pct >= 100) {
                        status_txt = "<span style='color:#22c55e;'>✅ BATEU META</span>";
                        agg.count_bateu_meta = (agg.count_bateu_meta || 0) + 1;
                    } else if (total_pct > 50) {
                        status_txt = "<span style='color:#f59e0b;'>⚠️ FORA DA META</span>";
                    } else {
                        status_txt = "<span style='color:#ef4444;'>❌ FORA DA META</span>";
                    }"""
    
    replacement = """                    if (bateu === 1) {
                        status_txt = "<span style='color:#22c55e;'>✅ BATEU META</span>";
                        agg.count_bateu_meta = (agg.count_bateu_meta || 0) + 1;
                    } else {
                        if (total_pct > 50) {
                            status_txt = "<span style='color:#f59e0b;'>⚠️ FORA DA META</span>";
                        } else {
                            status_txt = "<span style='color:#ef4444;'>❌ FORA DA META</span>";
                        }
                    }"""

    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
