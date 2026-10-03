import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject the new Data Blocks into the PDV Details
    target_inner_html = """                        inner_html += `<div style="margin-top:15px; font-weight:bold;">📦 Mix de Produtos (Core)</div>"""
    
    # We will insert the new blocks right before the Mix de Produtos table, or right after. The user says: 
    # "Quando o vendedor clicar em um PDV da lista para abrir a visão detalhada / estratégia: 1. Novo Bloco: Faturamento... 2. Novo Bloco: Execução..."
    # Let's put it right at the end of inner_html, after the Mix table, or before? Before the Mix table is better, right after the progress bars.
    
    # Wait, the user has Mix de Produtos (High End) and Mix de Produtos (Core). I'll find the place right before the `<details>` insertion, which is generic for both.
    
    target_details = """                    html_lista += `
                    <details class="pdv-row pdv-item\""""
                    
    replacement_details = """                    
                    // --- NOVOS DADOS DE FATURAMENTO E EXECUÇÃO ---
                    let meta_task = parseFloat(row['META TASK']) || 0;
                    let real_task = parseFloat(row['REAL TASK']) || 0;
                    let possui_task = row['POSSUI TASK'] ? row['POSSUI TASK'].trim().toUpperCase() : 'N';
                    let comprador = parseInt(row['COMPR']) || 0;
                    let coolers = parseInt(row['COOLERS']) || 0;
                    let mat_trade = row['MAT TRADE'] ? row['MAT TRADE'].trim() : '';
                    let dig_coup = row['DIG COUP'] ? row['DIG COUP'].trim() : '';
                    let cerv_tend = row['CERV (TEND)'] ? row['CERV (TEND)'].trim() : '';
                    let he_tend = row['HE (TEND)'] ? row['HE (TEND)'].trim() : '';

                    let fat_html = `<div style="margin-top: 20px; padding-top: 15px; border-top: 1px dashed ${border_color};">
                        <div style="font-weight: bold; margin-bottom: 10px;">🎯 Faturamento & BEES Force</div>
                        <div style="display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
                            ${comprador === 1 ? '<span style="background:rgba(34,197,94,0.2); color:#22c55e; border:1px solid #22c55e; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">✅ Comprador no Mês</span>' : '<span style="background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid #ef4444; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🚨 Não Comprador (NC)</span>'}
                            ${cerv_tend ? `<span style="background:rgba(255,255,255,0.05); border:1px solid ${border_color}; padding:4px 8px; border-radius:4px; font-size:0.8rem;">🍺 Cerveja: ${cerv_tend} vs LY</span>` : ''}
                            ${he_tend ? `<span style="background:rgba(255,255,255,0.05); border:1px solid ${border_color}; padding:4px 8px; border-radius:4px; font-size:0.8rem;">💎 High End: ${he_tend} vs LY</span>` : ''}
                        </div>`;

                    if (possui_task === 'S') {
                        let pct_task = meta_task > 0 ? (real_task / meta_task) * 100 : (real_task > 0 ? 100 : 0);
                        fat_html += barraHTML(pct_task, `💪 Desafio BEES Force — Meta: R$ ${meta_task.toFixed(2)} | Real: R$ ${real_task.toFixed(2)} | Falta: R$ ${Math.max(0, meta_task - real_task).toFixed(2)}`);
                    } else {
                        fat_html += `<div style="font-size: 0.85rem; color: #888; font-style: italic;">Sem task ativa no BEES Force.</div>`;
                    }
                    fat_html += `</div>`;

                    let exec_html = `<div style="margin-top: 15px;">
                        <div style="font-weight: bold; margin-bottom: 10px;">🧊 Execução no PDV & Trade</div>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <span style="background:rgba(59,130,246,0.2); color:#3b82f6; border:1px solid #3b82f6; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">❄️ ${coolers} Geladeira(s) Ambev</span>
                            ${mat_trade ? `<span style="background:rgba(168,85,247,0.2); color:#a855f7; border:1px solid #a855f7; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🎨 Trade: ${mat_trade}</span>` : ''}
                            ${dig_coup ? `<span style="background:rgba(234,179,8,0.2); color:#eab308; border:1px solid #eab308; padding:4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">🎫 Cupom Digital: ${dig_coup}</span>` : ''}
                        </div>
                    </div>`;
                    
                    let copiloto_data_str = encodeURIComponent(JSON.stringify({
                        nome: row['NOME PDV'],
                        comprador: comprador,
                        possui_task: possui_task,
                        meta_task: meta_task,
                        real_task: real_task,
                        coolers: coolers
                    }));

                    let btn_copiloto = `<div style="margin-top: 20px; text-align: center;">
                        <button onclick="prepararCopiloto('${copiloto_data_str}')" style="background: #6366f1; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">🤖 Gerar Tática no Copiloto</button>
                    </div>`;

                    inner_html += fat_html + exec_html + btn_copiloto;

                    html_lista += `
                    <details class="pdv-row pdv-item\""""
    html = html.replace(target_details, replacement_details)


    # 2. Add the function `prepararCopiloto` to global scope, just before `function getRawPrompt()`
    target_prompt = "function getRawPrompt() {"
    replacement_prompt = """window.pdvContextoCopiloto = null;
        function prepararCopiloto(dataStr) {
            const data = JSON.parse(decodeURIComponent(dataStr));
            window.pdvContextoCopiloto = data;
            
            // Preenche o campo de cliente automaticamente
            const clienteInput = document.getElementById('cliente');
            if (clienteInput) clienteInput.value = data.nome;
            
            // Rola a tela suavemente até a seção do Copiloto
            const copilotSection = document.getElementById('copiloto-section');
            if (copilotSection) copilotSection.scrollIntoView({ behavior: 'smooth' });
        }

        function getRawPrompt() {"""
    html = html.replace(target_prompt, replacement_prompt)

    # 3. Modify `getRawPrompt()` to inject the AI rules based on `window.pdvContextoCopiloto`
    target_rules = """REGRAS DE OURO TÁTICAS:
1. SEM ENROLAÇÃO TÉCNICA. O cliente não tem tempo.
2. ARGUMENTO MATEMÁTICO. Quebre a objeção focando no Lucro rápido ou Custo de Oportunidade.
3. GATILHO DE ESCASSEZ. Use o horário de corte do sistema de entrega para criar senso de urgência.
4. FECHAMENTO DUPLA ALTERNATIVA. O cliente não pode dizer "não". Ele deve escolher entre A ou B ("Quinta ou Sexta?")."""

    replacement_rules = """REGRAS DE OURO TÁTICAS:
1. SEM ENROLAÇÃO TÉCNICA. O cliente não tem tempo.
2. ARGUMENTO MATEMÁTICO. Quebre a objeção focando no Lucro rápido ou Custo de Oportunidade.
3. GATILHO DE ESCASSEZ. Use o horário de corte do sistema de entrega para criar senso de urgência.
4. FECHAMENTO DUPLA ALTERNATIVA. O cliente não pode dizer "não". Ele deve escolher entre A ou B ("Quinta ou Sexta?").`;

            // INJEÇÃO DINÂMICA DE DADOS DO PDV (FATURAMENTO E EXECUÇÃO)
            if (window.pdvContextoCopiloto && window.pdvContextoCopiloto.nome === cliente) {
                const pdv = window.pdvContextoCopiloto;
                let instrucoes_extras = "\\n\\nINSTRUÇÕES OBRIGATÓRIAS DE EXECUÇÃO NESTE PDV:\\n";
                
                if (pdv.comprador === 0) {
                    instrucoes_extras += "- PDV NÃO COMPRADOR NO MÊS: Sua prioridade tática absoluta é a Positivação de Segurança. Insira no argumento a necessidade de vender 1 cx de Cerveja Líder + 1 cx NAB para reativar.\\n";
                }
                if (pdv.possui_task === 'S' && pdv.real_task < pdv.meta_task) {
                    let falta_rs = (pdv.meta_task - pdv.real_task).toFixed(2);
                    instrucoes_extras += `- DESAFIO BEES FORCE ATIVO: Falta R$ ${falta_rs} para bater a meta da Task. Calcule rapidamente quantas caixas do produto foco cobrem esse valor e coloque essa matemática na fala de fechamento.\\n`;
                }
                if (pdv.coolers > 0) {
                    instrucoes_extras += `- GELADEIRA AMBEV PRESENTE (${pdv.coolers}): Lembre o cliente da regra de comodato (SOPI / Visibilidade). Use isso como alavanca de negociação se ele ameaçar colocar produto concorrente.\\n`;
                }
                promptFinal += instrucoes_extras;
            }

            promptFinal += `
FORMATO OBRIGATÓRIO (Exatamente 3 seções, marcadas com **Título**):"""

    # We need to rewrite the return statement to build promptFinal dynamically
    # So let's replace the whole function content properly.
    
    full_target_getraw = """            return `Você é o "Treinador de Elite", o mentor implacável da Ambev/BEES (o mesmo que avalia as simulações). Seu objetivo é dar a instrução tática final para o Vendedor (${vendedorPrimeiroNome}) quebrar a objeção ANTES de entrar no PDV. Você é direto, cirúrgico e focado em giro e margem.

DADOS DO CENÁRIO:
- Cliente: ${cliente} (Perfil: ${perfil} | Status: ${statusCompra})
- Produto Foco: ${produto} (Categoria: ${categoria})
- Objeção do Cliente: "${objecaoText}"
- Estilo do Vendedor: ${estilo}

REGRAS DE OURO TÁTICAS:
1. SEM ENROLAÇÃO TÉCNICA. O cliente não tem tempo.
2. ARGUMENTO MATEMÁTICO. Quebre a objeção focando no Lucro rápido ou Custo de Oportunidade.
3. GATILHO DE ESCASSEZ. Use o horário de corte do sistema de entrega para criar senso de urgência.
4. FECHAMENTO DUPLA ALTERNATIVA. O cliente não pode dizer "não". Ele deve escolher entre A ou B ("Quinta ou Sexta?").

FORMATO OBRIGATÓRIO (Exatamente 3 seções, marcadas com **Título**):

**Visão do Treinador:**
[Raio-X de 2 linhas: Qual o ponto fraco desse perfil de cliente e qual o erro fatal que o vendedor NÃO pode cometer aqui.]

**A Bala de Prata:**
"[A frase EXATA, matadora e persuasiva que o vendedor vai falar no balcão, de acordo com o estilo escolhido.]"

**Regra de Ouro:**
[A exigência que o vendedor deve pedir em troca (ponto extra, geladeira) e a pergunta matadora de fechamento por escolha dupla.]`;
        }"""

    full_replacement_getraw = """            let promptFinal = `Você é o "Treinador de Elite", o mentor implacável da Ambev/BEES (o mesmo que avalia as simulações). Seu objetivo é dar a instrução tática final para o Vendedor (${vendedorPrimeiroNome}) quebrar a objeção ANTES de entrar no PDV. Você é direto, cirúrgico e focado em giro e margem.

DADOS DO CENÁRIO:
- Cliente: ${cliente} (Perfil: ${perfil} | Status: ${statusCompra})
- Produto Foco: ${produto} (Categoria: ${categoria})
- Objeção do Cliente: "${objecaoText}"
- Estilo do Vendedor: ${estilo}

REGRAS DE OURO TÁTICAS:
1. SEM ENROLAÇÃO TÉCNICA. O cliente não tem tempo.
2. ARGUMENTO MATEMÁTICO. Quebre a objeção focando no Lucro rápido ou Custo de Oportunidade.
3. GATILHO DE ESCASSEZ. Use o horário de corte do sistema de entrega para criar senso de urgência.
4. FECHAMENTO DUPLA ALTERNATIVA. O cliente não pode dizer "não". Ele deve escolher entre A ou B ("Quinta ou Sexta?").`;

            if (window.pdvContextoCopiloto && window.pdvContextoCopiloto.nome === cliente) {
                const pdv = window.pdvContextoCopiloto;
                let instrucoes_extras = "\\n\\nINSTRUÇÕES OBRIGATÓRIAS DE EXECUÇÃO NESTE PDV:\\n";
                if (pdv.comprador === 0) {
                    instrucoes_extras += "- PDV NÃO COMPRADOR NO MÊS: Sua prioridade tática absoluta é a Positivação de Segurança. Insira no argumento a necessidade de vender 1 cx de Cerveja Líder + 1 cx NAB para reativar.\\n";
                }
                if (pdv.possui_task === 'S' && pdv.real_task < pdv.meta_task) {
                    let falta_rs = (pdv.meta_task - pdv.real_task).toFixed(2);
                    instrucoes_extras += `- DESAFIO BEES FORCE ATIVO: Falta R$ ${falta_rs} para bater a meta da Task. Calcule rapidamente quantas caixas do produto foco cobrem esse valor e coloque essa matemática na fala de fechamento.\\n`;
                }
                if (pdv.coolers > 0) {
                    instrucoes_extras += `- GELADEIRA AMBEV PRESENTE (${pdv.coolers}): Lembre o cliente da regra de comodato (SOPI / Visibilidade). Use isso como alavanca de negociação se ele ameaçar colocar produto concorrente.\\n`;
                }
                promptFinal += instrucoes_extras;
            }

            promptFinal += `\n\nFORMATO OBRIGATÓRIO (Exatamente 3 seções, marcadas com **Título**):

**Visão do Treinador:**
[Raio-X de 2 linhas: Qual o ponto fraco desse perfil de cliente e qual o erro fatal que o vendedor NÃO pode cometer aqui.]

**A Bala de Prata:**
"[A frase EXATA, matadora e persuasiva que o vendedor vai falar no balcão, de acordo com o estilo escolhido.]"

**Regra de Ouro:**
[A exigência que o vendedor deve pedir em troca (ponto extra, geladeira) e a pergunta matadora de fechamento por escolha dupla.]`;
            return promptFinal;
        }"""
    html = html.replace(full_target_getraw, full_replacement_getraw)

    # 4. Add id="copiloto-section" to the copilot container so scrollIntoView works
    # Search for "<h2>🤖 Copiloto de Vendas</h2>" and add ID to its parent or itself
    target_copiloto_h2 = "<h2>🤖 Copiloto de Vendas</h2>"
    replacement_copiloto_h2 = "<h2 id=\"copiloto-section\">🤖 Copiloto de Vendas</h2>"
    html = html.replace(target_copiloto_h2, replacement_copiloto_h2)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
