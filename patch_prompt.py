import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Rewriting getRawPrompt to be aggressive/assertive
    old_prompt_regex = r"function getRawPrompt\(\)\s*\{[\s\S]*?return[^;]+;\s*\}"
    
    new_prompt_func = """function getRawPrompt() {
            const vendedor = document.getElementById('vendedor-name').value || 'Representante Ambev';
            const vendedorPrimeiroNome = vendedor.split(' ')[0];
            const cliente = document.getElementById('cliente-name').value || 'Cliente';
            const categoria = document.getElementById('category-select').value;
            const produto = document.getElementById('product-select').value;
            const perfil = document.getElementById('persona-select').value;
            const statusCompra = document.getElementById('status-select').value;
            const objecaoText = document.getElementById('objection-select').options[document.getElementById('objection-select').selectedIndex].text;
            const estilo = document.getElementById('style-select').value;

            return `Você é um Treinador de Vendas de Elite da Ambev/BEES. Seu papel é dar ao vendedor (${vendedorPrimeiroNome}) um roteiro de balcão MATADOR, DIRETO e AGRESSIVO (no sentido comercial) para contornar a seguinte objeção: "${objecaoText}".

DADOS DO CENÁRIO:
- Cliente: ${cliente} (Perfil: ${perfil} | Status: ${statusCompra})
- Produto Foco: ${produto} (Categoria: ${categoria})
- Estilo do Vendedor: ${estilo}

REGRAS DE OURO (IGUAL AO SIMULADOR DE ROLEPLAY):
1. SEM ENROLAÇÃO. O cliente não tem tempo. Evite explicações teóricas.
2. FOCO EM GIRO E MARGEM. Quebre a objeção usando matemática simples (ex: "Se vender X no fim de semana, lucra Y").
3. GATILHO DE ESCASSEZ. Use o horário de corte do caminhão ou estoque limitado para pressionar o fechamento agora.
4. FECHAMENTO DUPLA ALTERNATIVA. Nunca faça perguntas de "sim/não". Dê opções ("Mando hoje à tarde ou amanhã cedo?").

FORMATO OBRIGATÓRIO DE RESPOSTA (Exatamente 3 Seções com Markdown **Título:**):

**🎯 Estratégia Mental (1 frase):**
Diga ao vendedor o ponto fraco desse perfil de cliente e o gatilho exato a ser usado.

**🗣️ Fala Pronta de Balcão:**
"[Escreva aqui a frase EXATA que o vendedor deve ler para o cliente. Curta, grossa, persuasiva, usando o estilo ${estilo}.]"

**🤝 Fechamento e Contrapartida:**
"[Escreva a pergunta final de dupla alternativa e o que exigir de exposição/trade no PDV.]"`;
        }"""
        
    html = re.sub(old_prompt_regex, new_prompt_func, html, flags=re.DOTALL)
    
    # Adding console.error to the catch block for debugging just in case
    old_catch = """} catch (error) {
                    alert("Erro na conexão com a IA: " + error.message);
                }"""
    new_catch = """} catch (error) {
                    console.error("Erro completo no fetch da IA:", error);
                    alert("Erro na conexão com a IA: " + error.message + "\\n\\nSe persistir, atualize a página (F5).");
                }"""
    html = html.replace(old_catch, new_catch)
    
    # Also adjust parseAIScript to handle the new titles easily
    old_parse = """if (/premissas|check/i.test(titleStr))               iconTitle = "📋 Check Rápido de Premissas & Cadastro";
                    else if (/abordagem|balcão/i.test(titleStr))         iconTitle = "🎯 Abordagem Direta de Balcão (Pronta para Usar)";
                    else if (/contrapartida|fechamento/i.test(titleStr))  iconTitle = "🤝 Contrapartida & Fechamento";
                    else iconTitle = titleStr;"""
                    
    new_parse = """if (/estratégia|mental/i.test(titleStr)) iconTitle = "🎯 Estratégia Mental Rápida";
                    else if (/fala|balcão/i.test(titleStr)) iconTitle = "🗣️ Fala Pronta (Leia para o Cliente)";
                    else if (/contrapartida|fechamento/i.test(titleStr)) iconTitle = "🤝 Fechamento de Venda";
                    else iconTitle = titleStr;"""
    html = html.replace(old_parse, new_parse)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
