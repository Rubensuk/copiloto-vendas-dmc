import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Trade Badges Zeroed Style
    target_badges = """let coolers_badge = coolers > 0 ? `<span style="background:rgba(59,130,246,0.2); color:#60a5fa; border:1px solid #3b82f6; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(59,130,246,0.3);">❄️ ${coolers} Geladeira(s) Ambev</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">❄️ 0 Geladeira(s)</span>`;
                    
                    let trade_val = mat_trade ? parseInt(mat_trade) : 0;
                    let cupom_val = dig_coup ? parseInt(dig_coup) : 0;
                    
                    let mat_trade_badge = trade_val > 0 ? `<span style="background:rgba(168,85,247,0.2); color:#c084fc; border:1px solid #a855f7; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(168,85,247,0.3);">🎨 Trade: ${trade_val}</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">🎨 Trade: 0</span>`;
                    
                    let dig_coup_badge = cupom_val > 0 ? `<span style="background:rgba(234,179,8,0.2); color:#facc15; border:1px solid #eab308; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(234,179,8,0.3);">🎫 Cupom Digital: ${cupom_val}</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">🎫 Cupom Digital: 0</span>`;"""
                    
    replacement_badges = """let inactive_style = `background:rgba(30, 41, 59, 0.8); color:#cbd5e1; border:1px solid rgba(71, 85, 105, 0.6); padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:500;`;
                    
                    let coolers_badge = coolers > 0 ? `<span style="background:rgba(59,130,246,0.2); color:#60a5fa; border:1px solid #3b82f6; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(59,130,246,0.3);">❄️ ${coolers} Geladeira(s) Ambev</span>` : `<span style="${inactive_style}">❄️ 0 Geladeiras</span>`;
                    
                    let trade_val = mat_trade ? parseInt(mat_trade) : 0;
                    let cupom_val = dig_coup ? parseInt(dig_coup) : 0;
                    
                    let mat_trade_badge = trade_val > 0 ? `<span style="background:rgba(168,85,247,0.2); color:#c084fc; border:1px solid #a855f7; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(168,85,247,0.3);">🎨 Trade: ${trade_val}</span>` : `<span style="${inactive_style}">🎨 Trade: 0</span>`;
                    
                    let dig_coup_badge = cupom_val > 0 ? `<span style="background:rgba(234,179,8,0.2); color:#facc15; border:1px solid #eab308; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(234,179,8,0.3);">🎫 Cupom Digital: ${cupom_val}</span>` : `<span style="${inactive_style}">🎟️ Cupom Digital: 0</span>`;"""

    html = html.replace(target_badges, replacement_badges)

    # 2. Add bottom padding to the details content container
    target_container = """<div style="padding: 15px; border-top: 1px solid rgba(255,255,255,0.05);">
                        ${inner_html}
                        ${fat_html}
                        ${exec_html}
                        ${btn_copiloto}
                    </div>"""
    
    replacement_container = """<div style="padding: 15px; padding-bottom: 25px; border-top: 1px solid rgba(255,255,255,0.05);">
                        ${inner_html}
                        ${fat_html}
                        ${exec_html}
                        ${btn_copiloto}
                    </div>"""

    html = html.replace(target_container, replacement_container)
    
    # 3. Ensure margin for btn_copiloto
    target_btn = """let btn_copiloto = `<div style="margin-top: 20px; text-align: center;">"""
    replacement_btn = """let btn_copiloto = `<div style="margin-top: 24px; margin-bottom: 8px; text-align: center;">"""
    html = html.replace(target_btn, replacement_btn)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
