import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove the old bad injection exactly
    bad_code = """
                        let insight = "";
                        if (real_int < meta_int) insight = "Falta vender " + (meta_int - real_int) + " cx de 600ml.";
                        else if (real_rgb < meta_rgb) insight = "Falta vender " + (meta_rgb - real_rgb) + " cx de Vasilhame (RGB).";
                        else if (real_300 < meta_300) insight = "Falta vender " + (meta_300 - real_300) + " cx de 300ml.";
                        
                        if (insight !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight}</div>` + inner_html;
                        }
                        """
    html = html.replace(bad_code, "")

    # 2. Inject proper HIGH END insight
    he_target = "inner_html += barraHTML(pct_600"
    he_insight = """
                        let insight_he = "";
                        if (real_600 < meta_600) insight_he = "Falta vender " + (meta_600 - real_600) + " cx de 600ml.";
                        else if (real_ln < meta_ln) insight_he = "Falta vender " + (meta_ln - real_ln) + " cx de Long Neck.";
                        
                        if (insight_he !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_he}</div>` + inner_html;
                        }
                        """
    html = html.replace(he_target, he_insight + he_target)

    # 3. Inject proper CORE insight
    core_target = "inner_html += barraHTML(pct_int"
    core_insight = """
                        let insight_core = "";
                        if (real_int < meta_int) insight_core = "Falta vender " + (meta_int - real_int) + " cx de Inteira (600ml).";
                        else if (real_rgb < meta_rgb) insight_core = "Falta vender " + (meta_rgb - real_rgb) + " cx de Vasilhame (RGB).";
                        else if (real_300 < meta_300) insight_core = "Falta vender " + (meta_300 - real_300) + " cx de 300ml.";
                        
                        if (insight_core !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_core}</div>` + inner_html;
                        }
                        """
    html = html.replace(core_target, core_insight + core_target)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
