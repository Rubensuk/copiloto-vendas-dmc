import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="DMC Sales Copilot - Metas & Portfólio", layout="wide")
st.title("🎯 DMC Sales Copilot — Metas & Portfólio (Araguaína/TO • Com TO PA Sul)")

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

def barra_progresso_html(percentual, label=""):
    """Gera uma barra de progresso com gradiente vermelho→amarelo→verde."""
    pct = min(max(percentual, 0), 100)
    if pct < 40:
        cor = '#ef4444'   # vermelho
    elif pct < 75:
        cor = '#f59e0b'   # amarelo
    else:
        cor = '#22c55e'   # verde

    html = f"""
    <div style="margin: 4px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 2px;">
            <span><b>{label}</b></span>
            <span style="color: {cor}; font-weight: 700;">{pct:.0f}%</span>
        </div>
        <div style="background: #2a2a3a; border-radius: 6px; height: 18px; overflow: hidden;">
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

m1, m2, m3 = st.columns(3)

pct_rgb = (real_rgb_total / meta_rgb_total * 100) if meta_rgb_total > 0 else 0
pct_600 = ((real_600_he + real_int_core) / (meta_600_he + meta_int_core) * 100) if (meta_600_he + meta_int_core) > 0 else 0
pct_ln  = (real_ln_total / meta_ln_total * 100) if meta_ln_total > 0 else 0

with m1:
    st.metric("📦 RGB (Vasilhames)", f"{real_rgb_total}/{meta_rgb_total} cxs")
    st.markdown(barra_progresso_html(pct_rgb, "Atingimento RGB"), unsafe_allow_html=True)

with m2:
    st.metric("🍺 600ml (Inteira + HE)", f"{real_600_he + real_int_core}/{meta_600_he + meta_int_core} SKUs")
    st.markdown(barra_progresso_html(pct_600, "Atingimento 600ml"), unsafe_allow_html=True)

with m3:
    st.metric("🍾 Long Neck", f"{real_ln_total}/{meta_ln_total} cxs")
    st.markdown(barra_progresso_html(pct_ln, "Atingimento Long Neck"), unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# MATRIZ DE CLIENTES COM BARRAS E PORTFÓLIO VISUAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📋 Clientes — Execução & Portfólio")

busca = st.text_input("🔍 Filtrar por Nome do PDV ou Chave:", "")
mostrar_fora = st.checkbox("Mostrar apenas quem está FORA da meta", value=False)

df_exib = df_rn.copy()
if busca:
    df_exib = df_exib[
        df_exib['NOME PDV'].astype(str).str.contains(busca, case=False, na=False) |
        df_exib['CHAVE PDV'].astype(str).str.contains(busca, case=False, na=False)
    ]
if mostrar_fora:
    df_exib = df_exib[df_exib['BATEU META'].fillna(0) == 0]

st.caption(f"Exibindo {len(df_exib)} de {total_pdvs} PDVs do RN {rn_selecionado}")

if df_exib.empty:
    st.info("Nenhum cliente encontrado.")
else:
    for _, row in df_exib.iterrows():
        base  = row.get('BASE', 'CORE')
        bateu = float(row.get('BATEU META', 0) or 0)
        status_txt = "✅ BATEU META" if bateu == 1 else "❌ FORA DA META"
        icone = "🟡" if base == 'CORE' else ("💎" if base == 'HIGH END' else "🏪")

        with st.expander(f"{icone} {row.get('NOME PDV', 'PDV')} — {base} — {status_txt}"):

            # ── INFO BÁSICA ────────────────────────────────────────────
            st.markdown(f"**Chave:** `{row.get('CHAVE PDV', '---')}` &nbsp;|&nbsp; **Visita:** {row.get('VISITA', '---')} &nbsp;|&nbsp; **Segmento:** {icone} {base}")
            st.markdown("---")

            # ══════════════════════════════════════════════════════════
            # BARRAS DE PROGRESSO — META vs REALIZADO
            # ══════════════════════════════════════════════════════════
            if base == 'HIGH END':
                meta_600  = float(row.get('600', 0) or 0)
                real_600  = float(row.get('REAL_HE_600', 0))
                meta_ln   = float(row.get('LN', 0) or 0)
                real_ln   = float(row.get('REAL_HE_LN', 0))

                pct_600 = (real_600 / meta_600 * 100) if meta_600 > 0 else 0
                pct_ln  = (real_ln / meta_ln * 100) if meta_ln > 0 else 0

                st.markdown("**📊 Progresso das Metas:**")
                st.markdown(
                    barra_progresso_html(pct_600, f"🍺 600ml — Meta: {int(meta_600)} | Real: {int(real_600)} | Falta: {int(max(0, meta_600 - real_600))}") +
                    barra_progresso_html(pct_ln,  f"🍾 Long Neck — Meta: {int(meta_ln)} | Real: {int(real_ln)} | Falta: {int(max(0, meta_ln - real_ln))}"),
                    unsafe_allow_html=True
                )

                # ── PORTFÓLIO VISUAL HIGH END ──────────────────────
                st.markdown("---")
                st.markdown("**📦 Portfólio 600ml:**")
                items_600 = []
                for col, nome in HE_600.items():
                    if col in df.columns:
                        val = row.get(col, 0)
                        vendeu = pd.notna(val) and float(val) > 0
                        items_600.append(quadrado_produto(nome, vendeu))
                if items_600:
                    st.markdown("<br>".join(items_600), unsafe_allow_html=True)

                st.markdown("**📦 Portfólio Long Neck:**")
                items_ln = []
                for col, nome in HE_LN.items():
                    if col in df.columns:
                        val = row.get(col, 0)
                        vendeu = pd.notna(val) and float(val) > 0
                        items_ln.append(quadrado_produto(nome, vendeu))
                if items_ln:
                    st.markdown("<br>".join(items_ln), unsafe_allow_html=True)

            elif base == 'CORE':
                meta_int = float(row.get('INTEIRA', 0) or 0)
                real_int = float(row.get('REAL_CORE_600', 0))
                meta_rgb = float(row.get('RGB', 0) or 0)
                real_rgb = float(row.get('REAL_RGB_TOTAL', 0))

                pct_int = (real_int / meta_int * 100) if meta_int > 0 else 0
                pct_rgb = (real_rgb / meta_rgb * 100) if meta_rgb > 0 else 0

                st.markdown("**📊 Progresso das Metas:**")
                st.markdown(
                    barra_progresso_html(pct_int, f"🍺 Inteira (600ml) — Meta: {int(meta_int)} | Real: {int(real_int)} | Falta: {int(max(0, meta_int - real_int))}") +
                    barra_progresso_html(pct_rgb, f"📦 RGB (Vasilhames) — Meta: {int(meta_rgb)} | Real: {int(real_rgb)} | Falta: {int(max(0, meta_rgb - real_rgb))}"),
                    unsafe_allow_html=True
                )

                # ── PORTFÓLIO VISUAL CORE ──────────────────────────
                st.markdown("---")
                st.markdown("**📦 Portfólio 600ml (Inteira):**")
                items_c600 = []
                for col, nome in CORE_600.items():
                    if col in df.columns:
                        val = row.get(col, 0)
                        vendeu = pd.notna(val) and float(val) > 0
                        items_c600.append(quadrado_produto(nome, vendeu))
                if items_c600:
                    st.markdown("<br>".join(items_c600), unsafe_allow_html=True)

                st.markdown("**📦 Portfólio 300ml:**")
                items_c300 = []
                for col, nome in CORE_300.items():
                    if col in df.columns:
                        val = row.get(col, 0)
                        vendeu = pd.notna(val) and float(val) > 0
                        items_c300.append(quadrado_produto(nome, vendeu))
                if items_c300:
                    st.markdown("<br>".join(items_c300), unsafe_allow_html=True)

                st.markdown("**📦 Portfólio 1000ml (Litrão):**")
                items_c1000 = []
                for col, nome in CORE_1000.items():
                    if col in df.columns:
                        val = row.get(col, 0)
                        vendeu = pd.notna(val) and float(val) > 0
                        items_c1000.append(quadrado_produto(nome, vendeu))
                if items_c1000:
                    st.markdown("<br>".join(items_c1000), unsafe_allow_html=True)

            else:
                st.write("🏪 Segmento Vitrine")
