def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The missing parseAIScript function
    parse_func = """
        function parseAIScript(text) {
            if (!text || typeof text !== 'string') return [];
            const steps = [];
            
            const blockRegex = /\\*\\*([^*]+)\\*\\*[:\\s]*([\\s\\S]*?)(?=\\*\\*[^*]+\\*\\*|$)/g;
            let match;
            while ((match = blockRegex.exec(text)) !== null) {
                const titleStr = (match[1] || '').trim();
                let bodyStr = (match[2] || '').trim();
                bodyStr = bodyStr.replace(/^[:\\-\\*]+\\s*/, '').trim();
                
                if (titleStr && bodyStr) {
                    let iconTitle = titleStr;
                    if (/estratégia|mental/i.test(titleStr)) iconTitle = "🎯 Estratégia Mental Rápida";
                    else if (/fala|balcão/i.test(titleStr)) iconTitle = "🗣️ Fala Pronta (Leia para o Cliente)";
                    else if (/contrapartida|fechamento/i.test(titleStr)) iconTitle = "🤝 Fechamento de Venda";
                    else iconTitle = titleStr;

                    steps.push({ title: iconTitle, text: bodyStr });
                }
            }
            
            if (steps.length === 0) {
                const fallbackRegex = /(\\b(?:Seção|Bloco|Passo) \\d+:[^\\n]+)\\n([^]*?)(?=(?:Seção|Bloco|Passo) \\d+:|$)/gi;
                while ((match = fallbackRegex.exec(text)) !== null) {
                    const t = (match[1] || '').trim();
                    const b = (match[2] || '').trim();
                    if (t && b) steps.push({ title: t, text: b });
                }
            }

            if (steps.length === 0) {
                const blocks = text.split(/\\n{2,}/);
                blocks.forEach((block, index) => {
                    if (block.trim() && index < 3) {
                        steps.push({ title: `Seção ${index + 1}`, text: block.trim() });
                    }
                });
            }

            return steps;
        }

"""

    # Inject right before formatStepContent
    if 'function parseAIScript(text)' not in html:
        html = html.replace('function formatStepContent(text)', parse_func + '        function formatStepContent(text)')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
