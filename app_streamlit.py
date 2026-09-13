import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="DMC - Score 5", layout="wide")
st.title("🎯 DMC - Score 5")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
GDRIVE_FILE_ID    = "1RdtvJaS0S1jeSNgBoYZ86WzIfvEIKlo8"
GDRIVE_EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{GDRIVE_FILE_ID}/export?format=xlsx"

# ─────────────────────────────────────────────────────────────────────────────
# MAPEAMENTO DE SIGLAS → NOMES COMPLETOS
# ─────────────────────────────────────────────────────────────────────────────
MARCAS = {
    'SPT': 'Spaten',
    'STL': 'Stella Artois',
    'STL PG': 'Stella Puro Glúten',
    'BUD': 'Budweiser',
    'COR': 'Corona',
    'ORI': 'Original',
    'AP': 'Antarctica',
    'BC': 'Brahma',
    'SK': 'Skol',
    'MIC': 'Michelob Ultra',
    'OUTROS': 'Outros',
}

# ─────────────────────────────────────────────────────────────────────────────
# PORTFÓLIO POR SEGMENTO (coluna → nome do produto)
# ─────────────────────────────────────────────────────────────────────────────

# HIGH END — 600ml
HE_600 = {
    'SPT 600': 'Spaten 600ml',
    'STL 600': 'Stella Artois 600ml',
    'STL PG 600': 'Stella Puro Glúten 600ml',
    'BUD 600': 'Budweiser 600ml',
    'COR 600': 'Corona 600ml',
    'ORI 600 ': 'Original 600ml',
    'OUTROS 600': 'Outros 600ml',
}

# HIGH END — Long Neck
HE_LN = {
    'COR LN': 'Corona Long Neck',
    'STL LN': 'Stella Artois Long Neck',
    'STL PG LN': 'Stella Puro Glúten Long Neck',
    'SPT LN': 'Spaten Long Neck',
    'MIC LN': 'Michelob Ultra Long Neck',
    'OUTROS LN': 'Outros Long Neck',
    'BUD LN': 'Budweiser Long Neck',
}

# CORE — 600ml (Inteira)
CORE_600 = {
    'AP 600': 'Antarctica 600ml',
    'BC 600': 'Brahma 600ml',
    'BUD 600 ': 'Budweiser 600ml',
    'ORI 600': 'Original 600ml',
    'SK 600': 'Skol 600ml',
    'SPT 600 ': 'Spaten 600ml',
    'STL 600 ': 'Stella Artois 600ml',
    'STL PG 600 ': 'Stella Puro Glúten 600ml',
    ' OUTROS 600 ': 'Outros 600ml',
}

# CORE — 300ml
CORE_300 = {
    'AP 300': 'Antarctica 300ml',
    'BC 300': 'Brahma 300ml',
    'BUD 300': 'Budweiser 300ml',
    'ORI 300': 'Original 300ml',
    'SK 300': 'Skol 300ml',
    'OUTROS 300': 'Outros 300ml',
}

# CORE — 1000ml (Litrão)
CORE_1000 = {
    'AP 1000': 'Antarctica 1000ml',
    'BC 1000': 'Brahma 1000ml',
    'BUD 1000': 'Budweiser 1000ml',
    'ORI 1000': 'Original 1000ml',
    'SK 1000': 'Skol 1000ml',
    'OUTROS 1000': 'Outros 1000ml',
}

# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────

def barra_progresso_html(percentual, label="", is_dark=True):
    """Gera uma barra de progresso com gradiente vermelho→amarelo→verde."""
    pct = min(max(percentual, 0), 100)
    if pct < 40:
        cor = '#ef4444'   # vermelho
    elif pct < 75:
        cor = '#f59e0b'   # amarelo
    else:
        cor = '#22c55e'   # verde

    bg_bar = "#2a2a3a" if is_dark else "#e2e8f0"

    html = f"""
    <div style="margin: 4px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 2px;">
            <span><b>{label}</b></span>
            <span style="color: {cor}; font-weight: 700;">{pct:.0f}%</span>
        </div>
        <div style="background: {bg_bar}; border-radius: 6px; height: 18px; overflow: hidden;">
            <div style="width: {pct}%; height: 100%; background: {cor}; border-radius: 6px; transition: width 0.3s;"></div>
        </div>
    </div>
    """
    return html


def quadrado_produto(nome, vendeu):
    """Quadrado verde (vendeu) ou vermelho (não vendeu) + nome do produto."""
    if vendeu:
        return f'<span style="display:inline-block;width:14px;height:14px;background:#22c55e;border-radius:3px;margin-right:6px;vertical-align:middle;"></span><span style="vertical-align:middle;">{nome}</span>'
    else:
        return f'<span style="display:inline-block;width:14px;height:14px;background:#ef4444;border-radius:3px;margin-right:6px;vertical-align:middle;"></span><span style="vertical-align:middle;">{nome}</span>'


# ─────────────────────────────────────────────────────────────────────────────
# CARREGAMENTO DA PLANILHA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def carregar_dados():
    try:
        resp = requests.get(GDRIVE_EXPORT_URL, timeout=30)
        if resp.status_code != 200:
            st.error(f"❌ Erro ao acessar Google Drive (status {resp.status_code}).")
            return pd.DataFrame()

        df = pd.read_excel(io.BytesIO(resp.content), sheet_name='Export')
        df['RN']   = pd.to_numeric(df['RN'], errors='coerce')
        df['BASE'] = df['BASE'].astype(str).str.strip().str.upper() if 'BASE' in df.columns else 'CORE'

        # ── Cálculos High End ──
        cols_he600 = [c for c in HE_600.keys() if c in df.columns]
        cols_heln  = [c for c in HE_LN.keys()  if c in df.columns]
        df['REAL_HE_600'] = df[cols_he600].fillna(0).sum(axis=1) if cols_he600 else 0
        df['REAL_HE_LN']  = df[cols_heln].fillna(0).sum(axis=1)  if cols_heln  else 0
        df['FALTA_HE_600'] = df.apply(lambda r: max(0, float(r.get('600',0) or 0) - float(r['REAL_HE_600'])), axis=1)
        df['FALTA_HE_LN']  = df.apply(lambda r: max(0, float(r.get('LN',0) or 0)  - float(r['REAL_HE_LN'])),  axis=1)

        # ── Cálculos Core RGB ──
        cols_c600  = [c for c in CORE_600.keys()  if c in df.columns]
        cols_c300  = [c for c in CORE_300.keys()  if c in df.columns]
        cols_c1000 = [c for c in CORE_1000.keys() if c in df.columns]
        df['REAL_CORE_600']  = df[cols_c600].fillna(0).sum(axis=1)  if cols_c600  else 0
        df['REAL_CORE_300']  = df[cols_c300].fillna(0).sum(axis=1)  if cols_c300  else 0
        df['REAL_CORE_1000'] = df[cols_c1000].fillna(0).sum(axis=1) if cols_c1000 else 0
        df['REAL_RGB_TOTAL'] = df['REAL_CORE_600'] + df['REAL_CORE_300'] + df['REAL_CORE_1000']
        df['FALTA_INTEIRA'] = df.apply(lambda r: max(0, float(r.get('INTEIRA',0) or 0) - float(r['REAL_CORE_600'])), axis=1)
        df['FALTA_RGB']     = df.apply(lambda r: max(0, float(r.get('RGB',0) or 0)     - float(r['REAL_RGB_TOTAL'])), axis=1)

        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

with st.spinner("📡 Conectando ao Google Drive..."):
    df = carregar_dados()

if st.button("🔄 Atualizar dados do Drive"):
    st.cache_data.clear()
    st.rerun()

if df.empty:
    st.warning("⚠️ Sem dados disponíveis.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# FILTRO DE RN
# ─────────────────────────────────────────────────────────────────────────────
rns_disponiveis = sorted([int(x) for x in df['RN'].dropna().unique()])

st.sidebar.header("🔍 Filtros de Operação")
rn_selecionado = st.sidebar.selectbox("Selecione o Roteiro (RN):", rns_disponiveis, format_func=lambda x: str(x))

df_rn   = df[df['RN'] == float(rn_selecionado)].copy()
df_core = df_rn[df_rn['BASE'] == 'CORE']
df_he   = df_rn[df_rn['BASE'] == 'HIGH END']

total_pdvs    = len(df_rn)
bateram_total = int(df_rn['BATEU META'].fillna(0).sum()) if 'BATEU META' in df_rn.columns else 0
bateram_core  = int(df_core['BATEU META'].fillna(0).sum()) if not df_core.empty else 0
bateram_he    = int(df_he['BATEU META'].fillna(0).sum()) if not df_he.empty else 0
fora_meta     = total_pdvs - bateram_total
score5_pct    = (bateram_total / total_pdvs * 100) if total_pdvs > 0 else 0.0

# ─────────────────────────────────────────────────────────────────────────────
# PAINEL EXECUTIVO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"### 📊 Painel Executivo — RN {rn_selecionado}")

# Linha 1: PDVs e Score 5
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("⭐ Score 5 (PDVs)", f"{bateram_total} de {total_pdvs}")
with c2: st.metric("🟡 PDVs Core", f"{len(df_core)}")
with c3: st.metric("💎 PDVs High End", f"{len(df_he)}")
with c4: st.metric("✅ Bateram Meta (Geral)", f"{bateram_total} PDVs")

st.markdown("")

# Linha 2: Meta consolidada da rota — quanto já bateu no geral
# RGB total (Core)
meta_rgb_total = int(df_core['RGB'].fillna(0).sum()) if not df_core.empty and 'RGB' in df_core.columns else 0
real_rgb_total = int(df_core['REAL_RGB_TOTAL'].sum()) if not df_core.empty else 0

# 600ml total (High End + Core Inteira)
meta_600_he    = int(df_he['600'].fillna(0).sum()) if not df_he.empty and '600' in df_he.columns else 0
real_600_he    = int(df_he['REAL_HE_600'].sum()) if not df_he.empty else 0
meta_int_core  = int(df_core['INTEIRA'].fillna(0).sum()) if not df_core.empty and 'INTEIRA' in df_core.columns else 0
real_int_core  = int(df_core['REAL_CORE_600'].sum()) if not df_core.empty else 0

# Long Neck total (High End)
meta_ln_total  = int(df_he['LN'].fillna(0).sum()) if not df_he.empty and 'LN' in df_he.columns else 0
real_ln_total  = int(df_he['REAL_HE_LN'].sum()) if not df_he.empty else 0

# 300ml total (Core)
real_300_total = int(df_core['REAL_CORE_300'].sum()) if not df_core.empty else 0
meta_300_total = int(df_core['LITRINHO'].fillna(0).sum()) if not df_core.empty and 'LITRINHO' in df_core.columns else 0

m1, m2, m3, m4 = st.columns(4)

pct_rgb = (real_rgb_total / meta_rgb_total * 100) if meta_rgb_total > 0 else 0
pct_600 = ((real_600_he + real_int_core) / (meta_600_he + meta_int_core) * 100) if (meta_600_he + meta_int_core) > 0 else 0
pct_ln  = (real_ln_total / meta_ln_total * 100) if meta_ln_total > 0 else 0
pct_300 = (real_300_total / meta_300_total * 100) if meta_300_total > 0 else 0

with m1:
    st.metric("📦 RGB (Vasilhames)", f"{real_rgb_total}/{meta_rgb_total} cxs")
    st.markdown(barra_progresso_html(pct_rgb, "Atingimento RGB", is_dark), unsafe_allow_html=True)

with m2:
    st.metric("🍺 600ml (Inteira + High End)", f"{real_600_he + real_int_core}/{meta_600_he + meta_int_core} SKUs")
    st.markdown(barra_progresso_html(pct_600, "Atingimento 600ml", is_dark), unsafe_allow_html=True)

with m3:
    st.metric("🍾 Long Neck", f"{real_ln_total}/{meta_ln_total} cxs")
    st.markdown(barra_progresso_html(pct_ln, "Atingimento Long Neck", is_dark), unsafe_allow_html=True)

with m4:
    st.metric("🥃 300ml", f"{real_300_total}/{meta_300_total} cxs")
    st.markdown(barra_progresso_html(pct_300, "Atingimento 300ml", is_dark), unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# LISTA DE CLIENTES COM META + TABELA DE MIX INLINE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📋 Clientes — Meta & Mix de Portfólio")

col_busca1, col_busca2 = st.columns([2, 1])
with col_busca1:
    busca = st.text_input("🔍 Filtrar por Nome do PDV ou Chave:", "")
with col_busca2:
    st.markdown("<br>", unsafe_allow_html=True)
    mostrar_fora = st.checkbox("Apenas FORA da meta", value=False)

# Filtro de Segmento (Botões para separar Core e High End)
segmento_filtro = st.radio(
    "Filtrar por Segmento:",
    ["Todos", "Core", "High End"],
    horizontal=True
)

df_exib = df_rn.copy()

if segmento_filtro == "Core":
    df_exib = df_exib[df_exib['BASE'] == 'CORE']
elif segmento_filtro == "High End":
    df_exib = df_exib[df_exib['BASE'] == 'HIGH END']

if busca:
    df_exib = df_exib[
        df_exib['NOME PDV'].astype(str).str.contains(busca, case=False, na=False) |
        df_exib['CHAVE PDV'].astype(str).str.contains(busca, case=False, na=False)
    ]
if mostrar_fora:
    df_exib = df_exib[df_exib['BATEU META'].fillna(0) == 0]

st.caption(f"Exibindo {len(df_exib)} de {total_pdvs} PDVs do RN {rn_selecionado}")

def gerar_quadrado(vendeu):
    cor = '#22c55e' if vendeu else '#ef4444'
    return f'<span style="display:inline-block;width:16px;height:16px;background:{cor};border-radius:3px;border:1px solid rgba(255,255,255,0.2);"></span>'

if df_exib.empty:
    st.info("Nenhum cliente encontrado.")
else:
    # ── CABEÇALHO DA TABELA DE CLIENTES ──
    header_html = f"""
    <div style="display:flex; padding:10px 15px; background:{html_bg_header}; font-weight:bold; font-size:0.9rem; border-bottom:2px solid {html_border}; margin-bottom:5px; color:{html_text};">
        <div style="flex: 2;">🏪 NOME DO PDV</div>
        <div style="flex: 1;">📊 SEGMENTO</div>
        <div style="flex: 1;">🎯 STATUS</div>
        <div style="flex: 2; text-align:right;">📋 METAS</div>
    </div>
    """
    
    html_lista = [header_html]

    for _, row in df_exib.iterrows():
        base  = row.get('BASE', 'CORE')
        bateu = float(row.get('BATEU META', 0) or 0)
        status_txt = "<span style='color:#22c55e;'>✅ BATEU META</span>" if bateu == 1 else "<span style='color:#ef4444;'>❌ FORA DA META</span>"
        icone = "🟡" if base == 'CORE' else ("💎" if base == 'HIGH END' else "🏪")

        # Função segura para lidar com NaN e converter para int
        def safe_int(v):
            return int(float(v)) if pd.notna(v) and str(v).strip() != '' else 0

        if base == 'HIGH END':
            meta_info = f"600ml: {safe_int(row.get('600',0))} &nbsp;|&nbsp; Long Neck: {safe_int(row.get('LN',0))}"
        elif base == 'CORE':
            meta_info = f"Inteira: {safe_int(row.get('INTEIRA',0))} &nbsp;|&nbsp; RGB: {safe_int(row.get('RGB',0))} &nbsp;|&nbsp; 300ml: {safe_int(row.get('LITRINHO',0))}"
        else:
            meta_info = "Vitrine"

        # Conteúdo interno (barras e tabela de mix)
        inner_html = ""
        
        if base == 'HIGH END':
            meta_600  = safe_int(row.get('600', 0))
            real_600  = safe_int(row.get('REAL_HE_600', 0))
            meta_ln   = safe_int(row.get('LN', 0))
            real_ln   = safe_int(row.get('REAL_HE_LN', 0))

            pct_600_c = (real_600 / meta_600 * 100) if meta_600 > 0 else 0
            pct_ln_c  = (real_ln / meta_ln * 100) if meta_ln > 0 else 0

            inner_html += barra_progresso_html(pct_600_c, f"🍺 600ml — Meta: {meta_600} | Real: {real_600} | Falta: {max(0, meta_600 - real_600)}", is_dark)
            inner_html += barra_progresso_html(pct_ln_c,  f"🍾 Long Neck — Meta: {meta_ln} | Real: {real_ln} | Falta: {max(0, meta_ln - real_ln)}", is_dark)

            mix_items = []
            def format_row(sq, nome, val):
                qtd = safe_int(val)
                return f'<tr style="border-bottom:1px solid {html_border};"><td style="padding:6px 12px;text-align:center;">{sq}</td><td style="padding:6px 12px;text-align:left;font-size:0.95rem;color:{html_text};">{nome}</td><td style="padding:6px 12px;text-align:center;font-weight:bold;color:{html_text};">{qtd}</td></tr>'

            for col, nome in HE_600.items():
                if col in df.columns:
                    val = row.get(col, 0)
                    vendeu = pd.notna(val) and safe_int(val) > 0
                    mix_items.append(format_row(gerar_quadrado(vendeu), nome, val))
            for col, nome in HE_LN.items():
                if col in df.columns:
                    val = row.get(col, 0)
                    vendeu = pd.notna(val) and safe_int(val) > 0
                    mix_items.append(format_row(gerar_quadrado(vendeu), nome, val))

            inner_html += f'''<div style="margin-top:15px; font-weight:bold; color:{html_text};">📦 Mix de Produtos (High End)</div>
            <table style="width:100%; border-collapse:collapse; margin-top:5px; background:{html_bg_header}; border-radius:5px; overflow:hidden;">
                <thead style="background:{html_bg_table_header};font-size:0.9rem;color:{html_text};">
                    <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                </thead>
                <tbody>{"".join(mix_items)}</tbody>
            </table>'''

        elif base == 'CORE':
            meta_int = safe_int(row.get('INTEIRA', 0))
            real_int = safe_int(row.get('REAL_CORE_600', 0))
            meta_rgb = safe_int(row.get('RGB', 0))
            real_rgb = safe_int(row.get('REAL_RGB_TOTAL', 0))
            meta_300 = safe_int(row.get('LITRINHO', 0))
            real_300 = safe_int(row.get('REAL_CORE_300', 0))

            pct_int_c = (real_int / meta_int * 100) if meta_int > 0 else 0
            pct_rgb_c = (real_rgb / meta_rgb * 100) if meta_rgb > 0 else 0
            pct_300_c = (real_300 / meta_300 * 100) if meta_300 > 0 else 0

            inner_html += barra_progresso_html(pct_int_c, f"🍺 Inteira (600ml) — Meta: {meta_int} | Real: {real_int} | Falta: {max(0, meta_int - real_int)}", is_dark)
            inner_html += barra_progresso_html(pct_rgb_c, f"📦 RGB (Vasilhames) — Meta: {meta_rgb} | Real: {real_rgb} | Falta: {max(0, meta_rgb - real_rgb)}", is_dark)
            inner_html += barra_progresso_html(pct_300_c, f"🥃 300ml — Meta: {meta_300} | Real: {real_300} | Falta: {max(0, meta_300 - real_300)}", is_dark)

            mix_items = []
            def format_row(sq, nome, val):
                qtd = safe_int(val)
                return f'<tr style="border-bottom:1px solid {html_border};"><td style="padding:6px 12px;text-align:center;">{sq}</td><td style="padding:6px 12px;text-align:left;font-size:0.95rem;color:{html_text};">{nome}</td><td style="padding:6px 12px;text-align:center;font-weight:bold;color:{html_text};">{qtd}</td></tr>'

            for col, nome in CORE_600.items():
                if col in df.columns:
                    val = row.get(col, 0)
                    vendeu = pd.notna(val) and safe_int(val) > 0
                    mix_items.append(format_row(gerar_quadrado(vendeu), nome, val))
            for col, nome in CORE_300.items():
                if col in df.columns:
                    val = row.get(col, 0)
                    vendeu = pd.notna(val) and safe_int(val) > 0
                    mix_items.append(format_row(gerar_quadrado(vendeu), nome, val))
            for col, nome in CORE_1000.items():
                if col in df.columns:
                    val = row.get(col, 0)
                    vendeu = pd.notna(val) and safe_int(val) > 0
                    mix_items.append(format_row(gerar_quadrado(vendeu), nome, val))

            inner_html += f'''<div style="margin-top:15px; font-weight:bold; color:{html_text};">📦 Mix de Produtos (Core)</div>
            <table style="width:100%; border-collapse:collapse; margin-top:5px; background:{html_bg_header}; border-radius:5px; overflow:hidden;">
                <thead style="background:{html_bg_table_header};font-size:0.9rem;color:{html_text};">
                    <tr><th style="padding:8px;text-align:center;width:15%;">Status</th><th style="padding:8px;text-align:left;width:65%;">Produto</th><th style="padding:8px;text-align:center;width:20%;">Vendida</th></tr>
                </thead>
                <tbody>{"".join(mix_items)}</tbody>
            </table>'''

        else:
            inner_html += f"<div style='color:{html_text};'>Segmento Vitrine</div>"

        # HTML do "Expander" (details/summary) customizado
        row_html = f"""
<details style="background: {html_bg_row}; border: 1px solid {html_border}; border-radius: 8px; margin-bottom: 8px; font-family: sans-serif; color: {html_text};">
    <summary style="padding: 12px 15px; cursor: pointer; display: flex; align-items: center; list-style: none;">
        <div style="flex: 2; font-weight: bold;">{icone} {row.get('NOME PDV', 'PDV')} <span style="font-size:0.75rem; color:#888; font-weight:normal; margin-left:5px;">{row.get('CHAVE PDV', '')}</span></div>
        <div style="flex: 1; font-size: 0.9rem;">{base}</div>
        <div style="flex: 1; font-size: 0.9rem; font-weight: bold;">{status_txt}</div>
        <div style="flex: 2; text-align: right; font-size: 0.9rem; color: #888;">{meta_info}</div>
    </summary>
    <div style="padding: 15px; border-top: 1px solid {html_border};">
        {inner_html}
    </div>
</details>
"""
        html_lista.append(row_html)

    # Renderiza tudo de uma vez
    st.markdown("".join(html_lista), unsafe_allow_html=True)

# CSS para esconder a setinha padrão do HTML details no Safari/Chrome
st.markdown("""
<style>
details > summary::-webkit-details-marker {
  display: none;
}
</style>
""", unsafe_allow_html=True)

