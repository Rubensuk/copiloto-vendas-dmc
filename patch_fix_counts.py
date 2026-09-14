import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix Papa.parse logic for data.meta
    old_kpi_logic = r"const kpis = parseInt\(row\['KPIs OK'\]\) \|\| 0;.*?if \(kpis === 5\) \{.*?consolidado\[rn\]\.meta \+= 1;.*?\}"
    new_kpi_logic = """const bateu = parseFloat(row['BATEU META']) || 0;
                            if (bateu === 1) {
                                consolidado[rn].meta += 1;
                            }"""
    html = re.sub(old_kpi_logic, new_kpi_logic, html, flags=re.DOTALL)
    
    # 2. Fix count_he and count_core updates
    old_he_check = "if (base === 'HIGH END') {"
    new_he_check = "if (base === 'HIGH END') {\n                        agg.count_he += 1;"
    html = html.replace(old_he_check, new_he_check)
    
    old_core_check = "} else if (base === 'CORE') {"
    new_core_check = "} else if (base === 'CORE') {\n                        agg.count_core += 1;"
    html = html.replace(old_core_check, new_core_check)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
