import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target = """                    let real_1000 = calcReal(row, CORE_1000);
                    let real_rgb = real_int + real_300 + real_1000;
                    
                    if (base === 'HIGH END') {"""

    replacement = """                    let real_1000 = calcReal(row, CORE_1000);
                    let real_rgb = real_int + real_300 + real_1000;
                    
                    let total_meta = base === 'HIGH END' ? (meta_600 + meta_ln) : (meta_int + meta_rgb + meta_300);
                    let total_real = base === 'HIGH END' ? (real_600 + real_ln) : (real_int + real_rgb + real_300);
                    let total_pct = total_meta > 0 ? (total_real / total_meta * 100) : (total_real > 0 ? 100 : 0);
                    
                    if (bateu === 1 || total_pct >= 100) {
                        status_txt = "<span style='color:#22c55e;'>✅ BATEU META</span>";
                    } else if (total_pct > 50) {
                        status_txt = "<span style='color:#f59e0b;'>⚠️ FORA DA META</span>";
                    } else {
                        status_txt = "<span style='color:#ef4444;'>❌ FORA DA META</span>";
                    }
                    
                    if (base === 'HIGH END') {"""

    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
