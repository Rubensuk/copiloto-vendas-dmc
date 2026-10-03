import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # --- PATCH HIGH END ---
    old_he = """                        let insight_he = "";
                        if (real_600 < meta_600) insight_he = "Falta vender " + (meta_600 - real_600) + " cx de 600ml.";
                        else if (real_ln < meta_ln) insight_he = "Falta vender " + (meta_ln - real_ln) + " cx de Long Neck.";
                        else if (real_ln_zero < meta_ln_zero) insight_he = "Falta vender " + (meta_ln_zero - real_ln_zero) + " cx de Long Neck Zero.";"""
                        
    new_he = """                        let faltas_he = [];
                        if (real_600 < meta_600) faltas_he.push((meta_600 - real_600) + " cx de 600ml");
                        if (real_ln < meta_ln) faltas_he.push((meta_ln - real_ln) + " cx de Long Neck");
                        if (real_ln_zero < meta_ln_zero) faltas_he.push((meta_ln_zero - real_ln_zero) + " cx de Long Neck Zero");
                        
                        let insight_he = "";
                        if (faltas_he.length > 0) {
                            insight_he = "Falta vender " + faltas_he.join(" + ") + ".";
                        }"""
    html = html.replace(old_he, new_he)

    # --- PATCH CORE ---
    old_core = """                        let insight_core = "";
                        if (real_int < meta_int) insight_core = "Falta vender " + (meta_int - real_int) + " cx de Inteira (600ml).";
                        else if (real_rgb < meta_rgb) insight_core = "Falta vender " + (meta_rgb - real_rgb) + " cx de Vasilhame (RGB).";
                        else if (real_300 < meta_300) insight_core = "Falta vender " + (meta_300 - real_300) + " cx de 300ml.";"""

    new_core = """                        let faltas_core = [];
                        if (real_int < meta_int) faltas_core.push((meta_int - real_int) + " cx de Inteira (600ml)");
                        if (real_rgb < meta_rgb) faltas_core.push((meta_rgb - real_rgb) + " cx de Vasilhame (RGB)");
                        if (real_300 < meta_300) faltas_core.push((meta_300 - real_300) + " cx de 300ml");
                        
                        let insight_core = "";
                        if (faltas_core.length > 0) {
                            insight_core = "Falta vender " + faltas_core.join(" + ") + ".";
                        }"""
    html = html.replace(old_core, new_core)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
