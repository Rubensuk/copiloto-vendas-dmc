import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Day of Week badge
    target_visita = """<div style="background: var(--tag-bg, rgba(255,255,255,0.1)); padding: 2px 6px; border-radius: 4px; font-size: 0.7rem;">${row['VISITA'] || ''}</div>"""
    replacement_visita = """<div style="background: var(--tag-bg, rgba(255,255,255,0.1)); padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight:600;">
                                ${(() => {
                                    const v = (row['VISITA'] || '').trim().toUpperCase();
                                    const map = {'SEG/':'🗓️ Seg', 'TER/':'🗓️ Terça', 'QUA/':'🗓️ Quarta', 'QUI/':'🗓️ Quinta', 'SEX/':'🗓️ Sexta', 'SAB/':'🗓️ Sábado', 'DOM/':'🗓️ Domingo'};
                                    return map[v] || '🗓️ ' + v;
                                })()}
                            </div>"""
    if target_visita in html:
        html = html.replace(target_visita, replacement_visita)
    else:
        # Fallback if the previous search failed because of slight differences
        html = re.sub(
            r'<div style="background: var\(--tag-bg, rgba\(255,255,255,0\.1\)\); padding: 2px 6px; border-radius: 4px; font-size: 0\.7rem;">\$\{row\[\'VISITA\'\] \|\| \'\'\}</div>',
            replacement_visita,
            html
        )

    # 2. miniCardHTML Helper injection
    if "function miniCardHTML" not in html:
        target_barraHTML = """function barraHTML(pct, label) {"""
        replacement_barraHTML = """
                function miniCardHTML(meta, real, label, icon) {
                    if (meta === 0 && real === 0) return '';
                    let pct = meta > 0 ? (real / meta * 100) : 100;
                    let falta = Math.max(0, meta - real);
                    let cor = pct <= 50 ? '#ef4444' : (pct < 100 ? '#f59e0b' : '#22c55e');
                    let tag = falta > 0 ? `<div style="background:rgba(239,68,68,0.2);color:#ef4444;padding:2px 6px;border-radius:4px;font-size:0.7rem;font-weight:bold;">Falta ${falta}</div>` : `<div style="background:rgba(34,197,94,0.2);color:#22c55e;padding:2px 6px;border-radius:4px;font-size:0.7rem;font-weight:bold;">Batida</div>`;
                    let bg_bar = document.body.classList.contains('light-mode') ? '#e2e8f0' : '#1e293b';
                    return `
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:10px; display:flex; flex-direction:column; justify-content: space-between; gap:6px; min-width: 0;">
                        <div style="font-size:0.8rem; color:var(--text-secondary); text-overflow: ellipsis; white-space: nowrap; overflow: hidden; font-weight:600;">${icon} ${label}</div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:1.15rem; font-weight:900; color:var(--text-primary);">${real} / ${meta}</span>
                            ${tag}
                        </div>
                        <div style="background:${bg_bar}; border-radius:4px; height:6px; overflow:hidden; margin-top:4px;">
                            <div style="width:${Math.min(pct, 100)}%; height:100%; background:${cor}; border-radius:4px;"></div>
                        </div>
                    </div>`;
                }
                function barraHTML(pct, label) {"""
        html = html.replace(target_barraHTML, replacement_barraHTML)

    # 3. HIGH END blocks replacement
    target_he_foco = """if (insight_he !== "" && bateu === 0) {
                            falta_volume_app = insight_he;
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_he}</div>` + inner_html;
                        }"""
    replacement_he_foco = """if (insight_he !== "" && bateu === 0) {
                            falta_volume_app = insight_he;
                            inner_html = `<div style="background: linear-gradient(145deg, #1e1b4b, #0f172a); border: 1px solid #f59e0b; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.15); padding: 12px; margin-bottom: 15px; border-radius: 8px;">
                                <div style="display:flex; align-items:center; gap:8px; font-weight:900; color:#f59e0b; margin-bottom:4px; font-size: 0.95rem;">
                                    <span>🎯</span> <span>Missão do Balcão</span>
                                </div>
                                <div style="font-size:1.05rem; font-weight:900; color:#fff; margin-bottom:4px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">${insight_he}</div>
                                <div style="font-size:0.75rem; color:#94a3b8; font-style:italic;">Destrave a meta e positive o mix High End deste cliente.</div>
                            </div>` + inner_html;
                        }"""
    html = html.replace(target_he_foco, replacement_he_foco)

    target_he_barras = """inner_html += barraHTML(pct_600, `🍺 600ml — Meta: ${meta_600} | Real: ${real_600} | Falta: ${Math.max(0, meta_600 - real_600)}`);
                        inner_html += barraHTML(pct_ln, `🍾 Long Neck — Meta: ${meta_ln} | Real: ${real_ln} | Falta: ${Math.max(0, meta_ln - real_ln)}`);
                        if (tem_zero) {
                            inner_html += barraHTML(pct_ln_zero, `🧊 Long Neck Zero — Meta: ${meta_ln_zero} | Real: ${real_ln_zero} | Falta: ${Math.max(0, meta_ln_zero - real_ln_zero)}`);
                        }"""
    replacement_he_barras = """let cards_he = `<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 12px;">`;
                        cards_he += miniCardHTML(meta_600, real_600, '600ml (HE)', '🍺');
                        cards_he += miniCardHTML(meta_ln, real_ln, 'Long Neck', '🍾');
                        if (tem_zero) cards_he += miniCardHTML(meta_ln_zero, real_ln_zero, 'LN Zero', '🧊');
                        cards_he += `</div>`;
                        inner_html += cards_he;"""
    html = html.replace(target_he_barras, replacement_he_barras)

    # 4. CORE blocks replacement
    target_core_foco = """if (insight_core !== "" && bateu === 0) {
                            falta_volume_app = insight_core;
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_core}</div>` + inner_html;
                        }"""
    replacement_core_foco = """if (insight_core !== "" && bateu === 0) {
                            falta_volume_app = insight_core;
                            inner_html = `<div style="background: linear-gradient(145deg, #1e1b4b, #0f172a); border: 1px solid #f59e0b; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.15); padding: 12px; margin-bottom: 15px; border-radius: 8px;">
                                <div style="display:flex; align-items:center; gap:8px; font-weight:900; color:#f59e0b; margin-bottom:4px; font-size: 0.95rem;">
                                    <span>🎯</span> <span>Missão do Balcão</span>
                                </div>
                                <div style="font-size:1.05rem; font-weight:900; color:#fff; margin-bottom:4px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">${insight_core}</div>
                                <div style="font-size:0.75rem; color:#94a3b8; font-style:italic;">Destrave a meta e positive o mix Core deste cliente.</div>
                            </div>` + inner_html;
                        }"""
    html = html.replace(target_core_foco, replacement_core_foco)

    target_core_barras = """inner_html += barraHTML(pct_int, `🍺 Inteira (600ml) — Meta: ${meta_int} | Real: ${real_int} | Falta: ${Math.max(0, meta_int - real_int)}`);
                        inner_html += barraHTML(pct_rgb, `📦 RGB (Vasilhames) — Meta: ${meta_rgb} | Real: ${real_rgb} | Falta: ${Math.max(0, meta_rgb - real_rgb)}`);
                        inner_html += barraHTML(pct_300, `🥃 300ml — Meta: ${meta_300} | Real: ${real_300} | Falta: ${Math.max(0, meta_300 - real_300)}`);"""
    replacement_core_barras = """let cards_core = `<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 12px;">`;
                        cards_core += miniCardHTML(meta_int, real_int, 'Inteira (600ml)', '🍺');
                        cards_core += miniCardHTML(meta_rgb, real_rgb, 'RGB', '📦');
                        cards_core += miniCardHTML(meta_300, real_300, '300ml', '🥃');
                        cards_core += `</div>`;
                        inner_html += cards_core;"""
    html = html.replace(target_core_barras, replacement_core_barras)

    # 5. Faturamento replacement
    target_fat = """let fat_html = `<div style="margin-top: 20px; padding-top: 15px; border-top: 1px dashed ${border_color};">
                        <div style="font-weight: bold; margin-bottom: 10px;">🎯 Faturamento</div>`;

                    if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        let formatBRL = (v) => v.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                        fat_html += barraHTML(pct_task, `💪 Faturamento — Meta: R$ ${formatBRL(meta_task)} | Real: R$ ${formatBRL(real_task)} | Falta: R$ ${formatBRL(Math.max(0, meta_task - real_task))}`);
                    } else {
                        fat_html += `<div style="font-size: 0.85rem; color: #888; font-style: italic;">Sem task ativa no BEES Force.</div>`;
                    }"""
    
    replacement_fat = """let fat_html = `<div style="margin-top: 20px; padding: 15px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);">`;

                    if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        let formatBRL = (v) => v.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                        let falta_v = Math.max(0, meta_task - real_task);
                        
                        fat_html += `<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <div style="font-weight: bold; color:var(--text-primary); font-size: 0.95rem;">🎯 Faturamento BEES Force</div>
                            ${falta_v === 0 ? `<span style="background:rgba(34,197,94,0.2); color:#22c55e; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:bold;">Concluído</span>` : `<span style="background:rgba(100,116,139,0.3); color:#cbd5e1; border:1px solid rgba(255,255,255,0.1); padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:bold;">${pct_task.toFixed(0)}%</span>`}
                        </div>`;
                        
                        fat_html += `<div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:6px;">Realizado: <span style="font-weight:900;color:#fff;">R$ ${formatBRL(real_task)}</span> / Meta: R$ ${formatBRL(meta_task)}</div>`;
                        
                        if (falta_v > 0) {
                            fat_html += `<div style="font-size:0.95rem; font-weight:900; color:#f97316; margin-bottom:10px; text-shadow:0 0 8px rgba(249,115,22,0.3);">Faltam apenas R$ ${formatBRL(falta_v)}</div>`;
                        } else {
                            fat_html += `<div style="font-size:0.95rem; font-weight:900; color:#22c55e; margin-bottom:10px;">Meta Atingida!</div>`;
                        }
                        
                        let cor_bar = pct_task <= 50 ? 'linear-gradient(90deg, #ef4444, #f97316)' : (pct_task < 100 ? 'linear-gradient(90deg, #f59e0b, #eab308)' : 'linear-gradient(90deg, #10b981, #22c55e)');
                        fat_html += `<div style="background:rgba(0,0,0,0.4); border-radius:6px; height:8px; overflow:hidden;">
                            <div style="width:${Math.min(pct_task, 100)}%; height:100%; background:${cor_bar}; border-radius:6px; transition: width 0.5s ease-in-out;"></div>
                        </div>`;
                        
                    } else {
                        fat_html += `<div style="font-weight: bold; color:var(--text-primary); font-size: 0.95rem; margin-bottom:4px;">🎯 Faturamento BEES Force</div>`;
                        fat_html += `<div style="font-size: 0.85rem; color: #64748b; font-style: italic;">Sem task ativa no BEES Force.</div>`;
                    }"""
    html = html.replace(target_fat, replacement_fat)

    # 6. Trade and Visita Execução Badges
    target_trade = """let coolers_badge = coolers > 0 ? `<span style="background:rgba(59,130,246,0.2); color:#3b82f6; border:1px solid #3b82f6; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">❄️ ${coolers} Geladeira(s) Ambev</span>` : '';
                    let mat_trade_badge = mat_trade ? `<span style="background:rgba(168,85,247,0.2); color:#a855f7; border:1px solid #a855f7; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🎨 Trade: ${mat_trade}</span>` : '';
                    let dig_coup_badge = dig_coup ? `<span style="background:rgba(234,179,8,0.2); color:#eab308; border:1px solid #eab308; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🎫 Cupom Digital: ${dig_coup}</span>` : '';
                    
                    let exec_html = '';
                    if (coolers_badge || mat_trade_badge || dig_coup_badge) {
                        exec_html = `<div style="margin-top: 15px;">
                            <div style="font-weight: bold; margin-bottom: 10px;">🧊 Execução no PDV & Trade</div>
                            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                ${coolers_badge}
                                ${mat_trade_badge}
                                ${dig_coup_badge}
                            </div>
                        </div>`;
                    }"""
    replacement_trade = """let coolers_badge = coolers > 0 ? `<span style="background:rgba(59,130,246,0.2); color:#60a5fa; border:1px solid #3b82f6; padding:4px 8px; border-radius:6px; font-size:0.8rem; font-weight:bold; box-shadow:0 0 8px rgba(59,130,246,0.3);">❄️ ${coolers} Geladeira(s) Ambev</span>` : `<span style="background:rgba(255,255,255,0.03); color:#64748b; border:1px solid rgba(255,255,255,0.05); padding:4px 8px; border-radius:6px; font-size:0.8rem; opacity:0.5;">❄️ 0 Geladeira(s)</span>`;
                    
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
    
    html = html.replace(target_trade, replacement_trade)

    # 7. Action Button Redesign
    target_btn = """let btn_copiloto = `<div style="margin-top: 20px; text-align: center;">
                        <button onclick="prepararCopiloto('${copiloto_data_str}')" style="background: #6366f1; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">🤖 Gerar Tática no Copiloto</button>
                    </div>`;"""
    
    replacement_btn = """let btn_copiloto = `<div style="margin-top: 20px; text-align: center;">
                        <button onclick="prepararCopiloto('${copiloto_data_str}')" style="background: linear-gradient(90deg, #4f46e5, #6366f1, #8b5cf6); background-size: 200% auto; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: 900; font-size: 1.05rem; cursor: pointer; width: 100%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); text-shadow: 0 1px 3px rgba(0,0,0,0.3); transition: all 0.3s ease; animation: gradientPulse 3s ease infinite;">🤖 Gerar Tática no Copiloto</button>
                    </div>`;"""
                    
    html = html.replace(target_btn, replacement_btn)
    
    # 8. Add pulse animation CSS
    if "keyframes gradientPulse" not in html:
        css_pulse = """
        @keyframes gradientPulse {
            0% { background-position: 0% 50%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); }
            50% { background-position: 100% 50%; box-shadow: 0 4px 20px rgba(139, 92, 246, 0.6); }
            100% { background-position: 0% 50%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); }
        }
        """
        html = html.replace("</style>", css_pulse + "</style>")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
