import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target_exec = """let exec_html = `<div style="margin-top: 15px;">
                        <div style="font-weight: bold; margin-bottom: 10px;">🧊 Execução no PDV & Trade</div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <span style="background:rgba(59,130,246,0.2); color:#3b82f6; border:1px solid #3b82f6; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">❄️ ${coolers} Geladeira(s) Ambev</span>
                            ${mat_trade ? `<span style="background:rgba(168,85,247,0.2); color:#a855f7; border:1px solid #a855f7; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🎨 Trade: ${mat_trade}</span>` : ''}
                            ${dig_coup ? `<span style="background:rgba(234,179,8,0.2); color:#eab308; border:1px solid #eab308; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🎫 Cupom Digital: ${dig_coup}</span>` : ''}
                        </div>
                    </div>`;"""
                    
    replacement_exec = """let coolers_badge = coolers > 0 ? `<span style="background:rgba(59,130,246,0.2); color:#60a5fa; border:1px solid #3b82f6; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(59,130,246,0.3);">❄️ ${coolers} Geladeira(s) Ambev</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">❄️ 0 Geladeira(s)</span>`;
                    
                    let trade_val = mat_trade ? parseInt(mat_trade) : 0;
                    let cupom_val = dig_coup ? parseInt(dig_coup) : 0;
                    
                    let mat_trade_badge = trade_val > 0 ? `<span style="background:rgba(168,85,247,0.2); color:#c084fc; border:1px solid #a855f7; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(168,85,247,0.3);">🎨 Trade: ${trade_val}</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">🎨 Trade: 0</span>`;
                    
                    let dig_coup_badge = cupom_val > 0 ? `<span style="background:rgba(234,179,8,0.2); color:#facc15; border:1px solid #eab308; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(234,179,8,0.3);">🎫 Cupom Digital: ${cupom_val}</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">🎫 Cupom Digital: 0</span>`;
                    
                    let exec_html = `<div style="margin-top: 20px;">
                        <div style="font-weight: bold; margin-bottom: 10px; font-size: 0.95rem;">🧊 Execução no PDV & Trade</div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            ${coolers_badge}
                            ${mat_trade_badge}
                            ${dig_coup_badge}
                        </div>
                    </div>`;"""
                    
    html = html.replace(target_exec, replacement_exec)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
