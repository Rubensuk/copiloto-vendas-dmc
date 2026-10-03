import re

def patch():
    # 1. Update sw.js version
    with open('sw.js', 'r', encoding='utf-8') as f:
        sw = f.read()
    sw = re.sub(r"const CACHE_NAME = 'dmc-copilot-v\d+';", "const CACHE_NAME = 'dmc-copilot-v10';", sw)
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(sw)

    # 2. Add try-catch and alerts to prepararCopiloto
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    target = """window.prepararCopiloto = function(dataStr) {
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
                const btnGen = document.getElementById('generate-btn');
                if (btnGen) {
                    btnGen.click();
                }
            }, 600);
        }"""
        
    replacement = """window.prepararCopiloto = function(dataStr) {
            try {
                const data = JSON.parse(decodeURIComponent(dataStr));
                window.pdvContextoCopiloto = data;
                
                const clienteInput = document.getElementById('cliente');
                if (clienteInput) clienteInput.value = data.nome;
                
                const copilotSection = document.getElementById('copiloto-section');
                if (copilotSection) copilotSection.scrollIntoView({ behavior: 'smooth' });
                
                setTimeout(() => {
                    const btnGen = document.getElementById('generate-btn');
                    if (btnGen) {
                        btnGen.click();
                    } else {
                        console.error('Botão generate-btn não encontrado!');
                    }
                }, 600);
            } catch (error) {
                console.error("Erro no prepararCopiloto:", error);
                alert("Erro ao preparar dados da IA: " + error.message);
            }
        }"""
        
    html = html.replace(target, replacement)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
