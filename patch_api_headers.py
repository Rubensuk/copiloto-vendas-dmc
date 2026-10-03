import re

def patch():
    with open('api/sheet.js', 'r', encoding='utf-8') as f:
        code = f.read()

    # The CSV processing logic to inject
    csv_processing = """
        let csvText = await response.text();
        
        // --- INÍCIO DO TRATAMENTO DE CABEÇALHOS DUPLICADOS ---
        let lines = csvText.split(/\\r?\\n/);
        if (lines.length > 0) {
            let headers = lines[0].split(',');
            // Índices 19 a 35 são High End (SPT 600 até OUTROS LN ZERO)
            for(let i = 19; i <= 35; i++) {
                if(headers[i]) headers[i] = 'HE_' + headers[i].trim();
            }
            // Índices 36 a 56 são Core (AP 600 até OUTROS 1000)
            for(let i = 36; i <= 56; i++) {
                if(headers[i]) headers[i] = 'CORE_' + headers[i].trim();
            }
            lines[0] = headers.join(',');
            csvText = lines.join('\\n');
        }
        // --- FIM DO TRATAMENTO ---
        """
        
    # Replace the simple csvText assignment
    old_csv_assign = "const csvText = await response.text();"
    
    if "TRATAMENTO DE CABEÇALHOS DUPLICADOS" not in code:
        code = code.replace(old_csv_assign, csv_processing)

    with open('api/sheet.js', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    patch()
