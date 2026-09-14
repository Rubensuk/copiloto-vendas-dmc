import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix Layout (Grid to Flex Column)
    old_layout = """        main {
            flex: 1;
            max-width: 1300px;
            width: 100%;
            margin: 2rem auto;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 2rem;
        }"""
    new_layout = """        main {
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 2rem auto;
            padding: 0 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }"""
    
    html = html.replace(old_layout, new_layout)
    
    # 2. Fix getRawPrompt logic to use actual correct elements
    old_prompt_regex = r"function getRawPrompt\(\)\s*\{[\s\S]*?return `Você é um Treinador de Vendas"
    
    new_prompt_func = """function getRawPrompt() {
            const vendedor = vendedorInput.value || 'Representante Ambev';
            const vendedorPrimeiroNome = vendedor.trim().split(' ')[0];
            const cliente = clienteInput.value || 'Cliente';
            const categoria = produtoSelect.options[produtoSelect.selectedIndex]?.getAttribute('data-category') || 'Bebidas';
            const produto = produtoSelect.options[produtoSelect.selectedIndex]?.text || '';
            const perfil = perfilClienteSelect.options[perfilClienteSelect.selectedIndex]?.text || '';
            const statusCompra = statusCompraSelect.options[statusCompraSelect.selectedIndex]?.text || '';
            
            let objecaoText = objecaoSelect.options[objecaoSelect.selectedIndex]?.text || '';
            if (objecaoSelect.value === 'custom') {
                objecaoText = customObjecaoInput.value || objecaoText;
            }
            
            const estilo = estiloVendedorSelect.options[estiloVendedorSelect.selectedIndex]?.text || '';

            return `Você é um Treinador de Vendas"""
            
    html = re.sub(old_prompt_regex, new_prompt_func, html, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
