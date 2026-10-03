import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target_exec = """let inactive_style = `background:rgba(30, 41, 59, 0.8); color:#cbd5e1; border:1px solid rgba(71, 85, 105, 0.6); padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:500;`;
                    
                    let coolers_badge = coolers > 0 ? `<span style="background:rgba(59,130,246,0.2); color:#60a5fa; border:1px solid #3b82f6; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(59,130,246,0.3);">❄️ ${coolers} Geladeira(s) Ambev</span>` : `<span style="${inactive_style}">❄️ 0 Geladeiras</span>`;
                    
                    let trade_val = mat_trade ? parseInt(mat_trade) : 0;
                    let cupom_val = dig_coup ? parseInt(dig_coup) : 0;
                    
                    let mat_trade_badge = trade_val > 0 ? `<span style="background:rgba(168,85,247,0.2); color:#c084fc; border:1px solid #a855f7; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(168,85,247,0.3);">🎨 Trade: ${trade_val}</span>` : `<span style="${inactive_style}">🎨 Trade: 0</span>`;
                    
                    let dig_coup_badge = cupom_val > 0 ? `<span style="background:rgba(234,179,8,0.2); color:#facc15; border:1px solid #eab308; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(234,179,8,0.3);">🎫 Cupom Digital: ${cupom_val}</span>` : `<span style="${inactive_style}">🎟️ Cupom Digital: 0</span>`;
                    
                    let exec_html = `<div style="margin-top: 20px;">
                        <div style="font-weight: bold; margin-bottom: 10px; font-size: 0.95rem;">🧊 Execução no PDV & Trade</div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            ${coolers_badge}
                            ${mat_trade_badge}
                            ${dig_coup_badge}
                        </div>
                    </div>`;"""
                    
    replacement_exec = """let trade_val = mat_trade ? parseInt(mat_trade) : 0;
                    let cupom_val = dig_coup ? parseInt(dig_coup) : 0;
                    
                    let card_coolers = coolers > 0 
                        ? `<div style="background:rgba(14,165,233,0.15); border:1px solid rgba(14,165,233,0.4); border-radius:12px; padding:10px; display:flex; flex-direction:column; justify-content:center; box-shadow:0 4px 10px rgba(14,165,233,0.1);">
                             <div style="font-size:0.65rem; color:var(--text-secondary); font-weight:bold; letter-spacing:0.5px; margin-bottom:4px;">COMODATO</div>
                             <div style="font-size:0.85rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:6px; margin-bottom:4px;">❄️ ${coolers} Geladeira(s)</div>
                             <div style="font-size:0.65rem; color:#10b981; font-weight:bold;">Ativo na Rota</div>
                           </div>`
                        : `<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(71,85,105,0.6); border-radius:12px; padding:10px; display:flex; flex-direction:column; justify-content:center;">
                             <div style="font-size:0.65rem; color:var(--text-secondary); font-weight:bold; letter-spacing:0.5px; margin-bottom:4px;">COMODATO</div>
                             <div style="font-size:0.85rem; font-weight:bold; color:#cbd5e1; display:flex; align-items:center; gap:6px; margin-bottom:4px;"><span style="filter:grayscale(1) opacity(0.5)">❄️</span> Sem Ativos</div>
                             <div style="font-size:0.65rem; color:#f59e0b; font-weight:bold;">Oportunidade</div>
                           </div>`;

                    let card_trade = trade_val > 0
                        ? `<div style="background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.4); border-radius:12px; padding:10px; display:flex; flex-direction:column; justify-content:center; box-shadow:0 4px 10px rgba(168,85,247,0.1);">
                             <div style="font-size:0.65rem; color:var(--text-secondary); font-weight:bold; letter-spacing:0.5px; margin-bottom:4px;">VISIBILIDADE</div>
                             <div style="font-size:0.85rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:6px; margin-bottom:4px;">🎨 Ativo (${trade_val})</div>
                             <div style="font-size:0.65rem; color:#10b981; font-weight:bold;">Positivado</div>
                           </div>`
                        : `<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(71,85,105,0.6); border-radius:12px; padding:10px; display:flex; flex-direction:column; justify-content:center;">
                             <div style="font-size:0.65rem; color:var(--text-secondary); font-weight:bold; letter-spacing:0.5px; margin-bottom:4px;">VISIBILIDADE</div>
                             <div style="font-size:0.85rem; font-weight:bold; color:#cbd5e1; display:flex; align-items:center; gap:6px; margin-bottom:4px;"><span style="filter:grayscale(1) opacity(0.5)">🎨</span> Sem Material</div>
                             <div style="font-size:0.65rem; color:#f59e0b; font-weight:bold;">Oportunidade</div>
                           </div>`;

                    let card_cupom = cupom_val > 0
                        ? `<div style="background:rgba(219,39,119,0.15); border:1px solid rgba(219,39,119,0.4); border-radius:12px; padding:10px; display:flex; flex-direction:column; justify-content:center; box-shadow:0 4px 10px rgba(219,39,119,0.1);">
                             <div style="font-size:0.65rem; color:var(--text-secondary); font-weight:bold; letter-spacing:0.5px; margin-bottom:4px;">DIGITAL BEES</div>
                             <div style="font-size:0.85rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:6px; margin-bottom:4px;">🎟️ ${cupom_val} Disponível</div>
                             <div style="font-size:0.65rem; color:#10b981; font-weight:bold;">Engajado</div>
                           </div>`
                        : `<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(71,85,105,0.6); border-radius:12px; padding:10px; display:flex; flex-direction:column; justify-content:center;">
                             <div style="font-size:0.65rem; color:var(--text-secondary); font-weight:bold; letter-spacing:0.5px; margin-bottom:4px;">DIGITAL BEES</div>
                             <div style="font-size:0.85rem; font-weight:bold; color:#cbd5e1; display:flex; align-items:center; gap:6px; margin-bottom:4px;"><span style="filter:grayscale(1) opacity(0.5)">🎟️</span> Sem Cupom</div>
                             <div style="font-size:0.65rem; color:#ef4444; font-weight:bold;">Não Ativado</div>
                           </div>`;

                    let exec_html = `<div style="margin-top: 24px; margin-bottom: 24px;">
                        <div style="font-weight: bold; margin-bottom: 12px; font-size: 0.95rem; color:var(--text-primary);">🧊 Execução no PDV & Trade</div>
                        <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px;">
                            ${card_coolers}
                            ${card_trade}
                            ${card_cupom}
                        </div>
                    </div>`;"""
                    
    html = html.replace(target_exec, replacement_exec)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
