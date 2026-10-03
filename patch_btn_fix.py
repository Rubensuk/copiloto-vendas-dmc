import re

def patch():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix the single quotes issue in copiloto_data_str
    target_encode = """let copiloto_data_str = encodeURIComponent(JSON.stringify({
                        nome: row['NOME PDV'],
                        comprador: comprador,
                        possui_task: possui_task,
                        meta_task: meta_task,
                        real_task: real_task,
                        coolers: coolers,
                        falta_volume: falta_volume_app
                    }));"""
    replacement_encode = """let copiloto_data_str = encodeURIComponent(JSON.stringify({
                        nome: row['NOME PDV'],
                        comprador: comprador,
                        possui_task: possui_task,
                        meta_task: meta_task,
                        real_task: real_task,
                        coolers: coolers,
                        falta_volume: falta_volume_app
                    })).replace(/'/g, "%27");"""
    html = html.replace(target_encode, replacement_encode)

    # 2. Fix the auto-generation function
    target_auto = """            // Auto-ativa o gerador de tática após 600ms
            setTimeout(() => {
                if (typeof gerarResposta === 'function') {
                    gerarResposta();
                }
            }, 600);"""
    replacement_auto = """            // Auto-ativa o gerador de tática após 600ms
            setTimeout(() => {
                const btnGen = document.getElementById('generate-btn');
                if (btnGen) {
                    btnGen.click();
                }
            }, 600);"""
    html = html.replace(target_auto, replacement_auto)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    patch()
