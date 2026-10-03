import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Define falta_volume_app right before the base check
    target1 = """                    let inner_html = '';
                    let meta_info = '';"""
    replacement1 = """                    let inner_html = '';
                    let meta_info = '';
                    let falta_volume_app = '';"""
    html = html.replace(target1, replacement1)

    # 2. Capture insight_he
    target2 = """                        if (insight_he !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_he}</div>` + inner_html;
                        }"""
    replacement2 = """                        if (insight_he !== "" && bateu === 0) {
                            falta_volume_app = insight_he;
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_he}</div>` + inner_html;
                        }"""
    html = html.replace(target2, replacement2)

    # 3. Capture insight_core
    target3 = """                        if (insight_core !== "" && bateu === 0) {
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_core}</div>` + inner_html;
                        }"""
    replacement3 = """                        if (insight_core !== "" && bateu === 0) {
                            falta_volume_app = insight_core;
                            inner_html = `<div style="background: rgba(255, 204, 0, 0.15); border-left: 3px solid #ffcc00; padding: 10px; margin-bottom: 12px; border-radius: 4px; font-weight: bold; color: #ffcc00; font-size: 0.9rem;">💡 Foco da Visita: ${insight_core}</div>` + inner_html;
                        }"""
    html = html.replace(target3, replacement3)

    # 4. Update the texts "🎯 Faturamento & BEES Force" and "💪 Desafio BEES Force"
    target4 = """let fat_html = `<div style="margin-top: 20px; padding-top: 15px; border-top: 1px dashed ${border_color};">
                        <div style="font-weight: bold; margin-bottom: 10px;">🎯 Faturamento & BEES Force</div>`;

                    if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        let formatBRL = (v) => v.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                        fat_html += barraHTML(pct_task, `💪 Desafio BEES Force — Meta: R$ ${formatBRL(meta_task)} | Real: R$ ${formatBRL(real_task)} | Falta: R$ ${formatBRL(Math.max(0, meta_task - real_task))}`);
                    } else {"""
                    
    replacement4 = """let fat_html = `<div style="margin-top: 20px; padding-top: 15px; border-top: 1px dashed ${border_color};">
                        <div style="font-weight: bold; margin-bottom: 10px;">🎯 Faturamento</div>`;

                    if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        let formatBRL = (v) => v.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                        fat_html += barraHTML(pct_task, `💪 Faturamento — Meta: R$ ${formatBRL(meta_task)} | Real: R$ ${formatBRL(real_task)} | Falta: R$ ${formatBRL(Math.max(0, meta_task - real_task))}`);
                    } else {"""
    html = html.replace(target4, replacement4)

    # 5. Add falta_volume_app to copiloto_data_str
    target5 = """let copiloto_data_str = encodeURIComponent(JSON.stringify({
                        nome: row['NOME PDV'],
                        comprador: comprador,
                        possui_task: possui_task,
                        meta_task: meta_task,
                        real_task: real_task,
                        coolers: coolers
                    }));"""
    replacement5 = """let copiloto_data_str = encodeURIComponent(JSON.stringify({
                        nome: row['NOME PDV'],
                        comprador: comprador,
                        possui_task: possui_task,
                        meta_task: meta_task,
                        real_task: real_task,
                        coolers: coolers,
                        falta_volume: falta_volume_app
                    }));"""
    html = html.replace(target5, replacement5)

    # 6. Auto-click Generate + Change the prompt rules
    target6 = """        function prepararCopiloto(dataStr) {
            const data = JSON.parse(decodeURIComponent(dataStr));
            window.pdvContextoCopiloto = data;
            
            // Preenche o campo de cliente automaticamente
            const clienteInput = document.getElementById('cliente');
            if (clienteInput) clienteInput.value = data.nome;
            
            // Rola a tela suavemente até a seção do Copiloto
            const copilotSection = document.getElementById('copiloto-section');
            if (copilotSection) copilotSection.scrollIntoView({ behavior: 'smooth' });
        }"""
    replacement6 = """        function prepararCopiloto(dataStr) {
            const data = JSON.parse(decodeURIComponent(dataStr));
            window.pdvContextoCopiloto = data;
            
            // Preenche o campo de cliente automaticamente
            const clienteInput = document.getElementById('cliente');
            if (clienteInput) clienteInput.value = data.nome;
            
            // Rola a tela suavemente até a seção do Copiloto
            const copilotSection = document.getElementById('copiloto-section');
            if (copilotSection) copilotSection.scrollIntoView({ behavior: 'smooth' });
            
            // Auto-ativa o gerador de tática após 600ms
            setTimeout(() => {
                if (typeof gerarResposta === 'function') {
                    gerarResposta();
                }
            }, 600);
        }"""
    html = html.replace(target6, replacement6)

    # 7. Update prompt payload
    target7 = """if (pdv.possui_task === 'S' && pdv.real_task < pdv.meta_task) {
                    let falta_rs = (pdv.meta_task - pdv.real_task).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                    instrucoes_extras += `- DESAFIO BEES FORCE ATIVO: Falta R$ ${falta_rs} para bater a meta da Task. Calcule rapidamente quantas caixas do produto foco cobrem esse valor e coloque essa matemática na fala de fechamento.\\n`;
                }"""
    replacement7 = """if (pdv.possui_task === 'S' && pdv.real_task < pdv.meta_task) {
                    let falta_rs = (pdv.meta_task - pdv.real_task).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                    instrucoes_extras += `- META DE FATURAMENTO: Faltam exatamente R$ ${falta_rs} para o vendedor bater a meta de faturamento neste cliente. Faça as contas de quantas caixas do produto foco cobrem esse valor e insira isso no fechamento.\\n`;
                }
                if (pdv.falta_volume) {
                    instrucoes_extras += `- GAP DE VOLUME (O QUE FALTA BATER): ${pdv.falta_volume}. O VENDEDOR SÓ BATE A META DA ROTA SE VENDER ISSO. Crie um argumento incisivo que empurre exatamente essa quantidade de caixas goela abaixo do cliente (de forma persuasiva e técnica).\\n`;
                }"""
    html = html.replace(target7, replacement7)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
