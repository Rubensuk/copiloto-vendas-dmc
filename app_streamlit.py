import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="DMC Sales Copilot - Metas & Portfólio", layout="wide")
st.title("🎯 DMC Sales Copilot — Metas & Portfólio (Araguaína/TO • Com TO PA Sul)")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DO GOOGLE DRIVE
# ─────────────────────────────────────────────────────────────────────────────
GDRIVE_FILE_ID    = "1RdtvJaS0S1jeSNgBoYZ86WzIfvEIKlo8"
GDRIVE_EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{GDRIVE_FILE_ID}/export?format=xlsx"

# ─────────────────────────────────────────────────────────────────────────────
# COLUNAS DE REALIZADO (High End e Core RGB)
# ─────────────────────────────────────────────────────────────────────────────
# HIGH END 600ml (positivação de SKUs)
HE_600_COLS = ['SPT 600', 'STL 600', 'STL PG 600', 'BUD 600', 'COR 600', 'ORI 600 ', 'OUTROS 600']
# HIGH END Long Necks
HE_LN_COLS  = ['COR LN', 'STL LN', 'STL PG LN', 'SPT LN', 'MIC LN', 'OUTROS LN', 'BUD LN']
# Core RGB (vasilhames retornáveis: 600 + 300 + 1000)
CORE_600_COLS = ['AP 600', 'BC 600', 'BUD 600 ', 'ORI 600', 'SK 600', 'SPT 600 ', 'STL 600 ', 'STL PG 600 ', ' OUTROS 600 ']
CORE_300_COLS = ['AP 300', 'BC 300', 'BUD 300', 'ORI 300', 'SK 300', 'OUTROS 300']
CORE_1000_COLS = ['AP 1000', 'BC 1000', 'BUD 1000', 'ORI 1000', 'SK 1000', 'OUTROS 1000']

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

        # Normaliza tipos
        df['RN']   = pd.to_numeric(df['RN'], errors='coerce')
        df['BASE'] = df['BASE'].astype(str).str.strip().str.upper() if 'BASE' in df.columns else 'CORE'

        # ── Cálculos High End ──────────────────────────────────────────
        cols_he600 = [c for c in HE_600_COLS if c in df.columns]
        cols_heln  = [c for c in HE_LN_COLS  if c in df.columns]

        df['REAL_HE_600'] = df[cols_he600].fillna(0).sum(axis=1) if cols_he600 else 0
        df['REAL_HE_LN']  = df[cols_heln].fillna(0).sum(axis=1)  if cols_heln  else 0

        df['FALTA_HE_600'] = df.apply(
            lambda r: max(0, float(r.get('600', 0) or 0) - float(r['REAL_HE_600'])), axis=1
        )
        df['FALTA_HE_LN'] = df.apply(
            lambda r: max(0, float(r.get('LN', 0) or 0) - float(r['REAL_HE_LN'])), axis=1
        )

        # ── Cálculos Core RGB (600 + 300 + 1000) ──────────────────────
        cols_c600  = [c for c in CORE_600_COLS  if c in df.columns]
        cols_c300  = [c for c in CORE_300_COLS  if c in df.columns]
        cols_c1000 = [c for c in CORE_1000_COLS if c in df.columns]

        df['REAL_CORE_600']  = df[cols_c600].fillna(0).sum(axis=1)  if cols_c600  else 0
        df['REAL_CORE_300']  = df[cols_c300].fillna(0).sum(axis=1)  if cols_c300  else 0
        df['REAL_CORE_1000'] = df[cols_c1000].fillna(0).sum(axis=1) if cols_c1000 else 0
        df['REAL_RGB_TOTAL'] = df['REAL_CORE_600'] + df['REAL_CORE_300'] + df['REAL_CORE_1000']

        # Falta Core Inteira (meta col INTEIRA vs realizado 600ml core)
        df['FALTA_INTEIRA'] = df.apply(
            lambda r: max(0, float(r.get('INTEIRA', 0) or 0) - float(r['REAL_CORE_600'])), axis=1
        )
        # Falta Core RGB (meta col RGB vs realizado total vasilhames)
        df['FALTA_RGB'] = df.apply(
            lambda r: max(0, float(r.get('RGB', 0) or 0) - float(r['REAL_RGB_TOTAL'])), axis=1
        )

        return df

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

with st.spinner("📡 Conectando ao Google Drive..."):
    df = carregar_dados()

if st.button("🔄 Atualizar dados do Drive"):
    st.cache_data.clear()
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# APLICAÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
if df.empty:
    st.warning("⚠️ Sem dados disponíveis.")
    st.stop()

# ── Filtro Dinâmico de RN ──────────────────────────────────────────────────
rns_disponiveis = sorted([int(x) for x in df['RN'].dropna().unique()])

st.sidebar.header("🔍 Filtros de Operação")
rn_selecionado = st.sidebar.selectbox(
    "Selecione o Roteiro (RN):",
    rns_disponiveis,
    format_func=lambda x: str(x)
)

# ── Filtragem rigorosa ─────────────────────────────────────────────────────
df_rn = df[df['RN'] == float(rn_selecionado)].copy()

# ── Segmentação ────────────────────────────────────────────────────────────
df_core = df_rn[df_rn['BASE'] == 'CORE']
df_he   = df_rn[df_rn['BASE'] == 'HIGH END']
df_vit  = df_rn[df_rn['BASE'] == 'VITRINE']

total_pdvs    = len(df_rn)
total_core    = len(df_core)
total_he      = len(df_he)
total_vit     = len(df_vit)

bateram_total = int(df_rn['BATEU META'].fillna(0).sum()) if 'BATEU META' in df_rn.columns else 0
bateram_core  = int(df_core['BATEU META'].fillna(0).sum()) if not df_core.empty and 'BATEU META' in df_core.columns else 0
bateram_he    = int(df_he['BATEU META'].fillna(0).sum()) if not df_he.empty and 'BATEU META' in df_he.columns else 0
fora_meta     = total_pdvs - bateram_total
score5_pct    = (bateram_total / total_pdvs * 100) if total_pdvs > 0 else 0.0

# ─────────────────────────────────────────────────────────────────────────────
# PAINEL EXECUTIVO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"### 📊 Painel Executivo — RN {rn_selecionado}")

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("⭐ Score 5 (%)", f"{score5_pct:.1f}%")
with c2: st.metric("🟡 Core", f"{bateram_core}/{total_core}")
with c3: st.metric("💎 High End", f"{bateram_he}/{total_he}")
with c4: st.metric("✅ Bateram", f"{bateram_total} PDVs")
with c5: st.metric("❌ Fora", f"{fora_meta} PDVs")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# GAP CONSOLIDADO POR SEGMENTO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"#### 📉 Gap Consolidado — RN {rn_selecionado}")

g1, g2, g3, g4 = st.columns(4)

if not df_core.empty:
    with g1: st.metric("🟡 Falta Core Inteira", f"{int(df_core['FALTA_INTEIRA'].sum())} SKUs")
    with g2: st.metric("🟡 Falta Core RGB", f"{int(df_core['FALTA_RGB'].sum())} cxs")

if not df_he.empty:
    with g3: st.metric("💎 Falta HE 600ml", f"{int(df_he['FALTA_HE_600'].sum())} SKUs")
    with g4: st.metric("💎 Falta HE Long Neck", f"{int(df_he['FALTA_HE_LN'].sum())} cxs")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# MATRIZ DE CONSULTA POR CLIENTE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📋 Matriz de Clientes — Execução Individual")

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
        base   = row.get('BASE', 'CORE')
        bateu  = float(row.get('BATEU META', 0) or 0)
        status = "✅ Bateu Meta" if bateu == 1 else "❌ Fora da Meta"
        icone  = "🟡" if base == 'CORE' else ("💎" if base == 'HIGH END' else "🏪")

        with st.expander(f"{icone} {row.get('NOME PDV', 'PDV')} — {base} — {status}"):
            c1, c2, c3 = st.columns(3)

            with c1:
                st.write(f"**Chave PDV:** `{row.get('CHAVE PDV', '---')}`")
                st.write(f"**Dia de Visita:** {row.get('VISITA', '---')}")
                st.write(f"**Segmento:** {icone} {base}")

            with c2:
                if base == 'HIGH END':
                    meta_600 = row.get('600', 0) or 0
                    real_600 = row.get('REAL_HE_600', 0)
                    falta_600 = row.get('FALTA_HE_600', 0)
                    meta_ln  = row.get('LN', 0) or 0
                    real_ln  = row.get('REAL_HE_LN', 0)
                    falta_ln = row.get('FALTA_HE_LN', 0)

                    st.write(f"**600ml** — Meta: `{int(meta_600)}` | Real: `{int(real_600)}` | Falta: `{int(falta_600)}`")
                    st.write(f"**Long Neck** — Meta: `{int(meta_ln)}` | Real: `{int(real_ln)}` | Falta: `{int(falta_ln)}`")
                elif base == 'CORE':
                    meta_int = row.get('INTEIRA', 0) or 0
                    meta_rgb = row.get('RGB', 0) or 0
                    real_600c = row.get('REAL_CORE_600', 0)
                    real_rgb  = row.get('REAL_RGB_TOTAL', 0)
                    falta_int = row.get('FALTA_INTEIRA', 0)
                    falta_rgb = row.get('FALTA_RGB', 0)

                    st.write(f"**Inteira (600ml)** — Meta: `{int(meta_int)}` | Real: `{int(real_600c)}` | Falta: `{int(falta_int)}`")
                    st.write(f"**RGB (Vasilhames)** — Meta: `{int(meta_rgb)}` | Real: `{int(real_rgb)}` | Falta: `{int(falta_rgb)}`")
                else:
                    st.write("Segmento Vitrine")

            with c3:
                st.write(f"**Status:** {status}")
                st.write(f"**Operação:** {row.get('OPERAÇÃO', '---')}")
