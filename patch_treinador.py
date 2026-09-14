import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update getRawPrompt to have the "Treinador do Simulador" DNA
    old_prompt_regex = r"return `Você é um Treinador de Vendas.*?\]\"`;"
    
    new_prompt_string = """return `Você é o "Treinador de Elite", o mentor implacável da Ambev/BEES (o mesmo que avalia as simulações). Seu objetivo é dar a instrução tática final para o Vendedor (${vendedorPrimeiroNome}) quebrar a objeção ANTES de entrar no PDV. Você é direto, cirúrgico e focado em giro e margem.

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
[A exigência que o vendedor deve pedir em troca (ponto extra, geladeira) e a pergunta matadora de fechamento por escolha dupla.]`;"""

    html = re.sub(old_prompt_regex, new_prompt_string, html, flags=re.DOTALL)
    
    # 2. Update parseAIScript mapping
    old_parse = """if (/estratégia|mental/i.test(titleStr)) iconTitle = "🎯 Estratégia Mental Rápida";
                    else if (/fala|balcão/i.test(titleStr)) iconTitle = "🗣️ Fala Pronta (Leia para o Cliente)";
                    else if (/contrapartida|fechamento/i.test(titleStr)) iconTitle = "🤝 Fechamento de Venda";
                    else iconTitle = titleStr;"""
                    
    new_parse = """if (/visão|treinador/i.test(titleStr)) iconTitle = "🧠 Visão do Treinador";
                    else if (/bala|prata/i.test(titleStr)) iconTitle = "🔥 A Bala de Prata (Fala Pronta)";
                    else if (/regra|ouro/i.test(titleStr)) iconTitle = "🏆 Regra de Ouro (Fechamento)";
                    else iconTitle = titleStr;"""
                    
    html = html.replace(old_parse, new_parse)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
