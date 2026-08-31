import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="DMC Sales Copilot - Metas & Portfólio", layout="wide")
st.title("🎯 DMC Sales Copilot — Metas & Portfólio (Araguaína/TO • Com TO PA Sul)")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DO GOOGLE DRIVE
# ─────────────────────────────────────────────────────────────────────────────
GDRIVE_FILE_ID   = "1WJOSePDmcVRjANuUXIuJLFdB8p0yhTvB"
GDRIVE_EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{GDRIVE_FILE_ID}/export?format=xlsx"

# KPIs que compõem o Score 5
KPIS = ['COMPR', 'VISITAÇÃO', 'TASK FAT', 'COOLERS', 'AD & TASK', 'MENU & PTC', 'MAT TRADE', 'DIG COUP']
KPIS_LABELS = {
    'COMPR'      : '🛒 Compra',
    'VISITAÇÃO'  : '👁️ Visitação',
    'TASK FAT'   : '📦 Task Fat.',
    'COOLERS'    : '❄️ Coolers',
    'AD & TASK'  : '📢 AD & Task',
    'MENU & PTC' : '📋 Menu & PTC',
    'MAT TRADE'  : '🎨 Mat. Trade',
    'DIG COUP'   : '🎟️ Dig. Coupon',
}

# ─────────────────────────────────────────────────────────────────────────────
# CARREGAMENTO E TRATAMENTO DA PLANILHA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def carregar_dados():
    try:
        resp = requests.get(GDRIVE_EXPORT_URL, timeout=30)
        if resp.status_code != 200:
            st.error(f"❌ Erro ao acessar Google Drive (status {resp.status_code}). Verifique o compartilhamento do arquivo.")
            return pd.DataFrame()

        df = pd.read_excel(io.BytesIO(resp.content), sheet_name='Export')

        # Normaliza tipos
        df['RN']   = pd.to_numeric(df['RN'],   errors='coerce')
        df['BASE'] = df['BASE'].astype(str).str.strip().str.upper() if 'BASE' in df.columns else 'CORE'

        # Score 5: cliente atingiu todos os 5 KPIs quando KPIs OK == 5
        df['BATEU_SCORE5'] = (df['KPIs OK'] == 5).astype(int) if 'KPIs OK' in df.columns else 0

        return df

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

with st.spinner("📡 Conectando ao Google Drive e carregando planilha..."):
    df = carregar_dados()

if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# APLICAÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
if df.empty:
    st.warning("⚠️ Sem dados disponíveis. Verifique a conexão com o Google Drive.")
    st.stop()

# ── Filtro de RN — apenas o número, lido dinamicamente ────────────────────
rns_disponiveis = sorted([int(x) for x in df['RN'].dropna().unique()])

st.sidebar.header("🔍 Filtros de Operação")
rn_selecionado = st.sidebar.selectbox(
    "Selecione o Roteiro (RN):",
    rns_disponiveis,
    format_func=lambda x: str(x)
)

# ── Filtragem rigorosa pelo RN selecionado ─────────────────────────────────
df_rn = df[df['RN'] == float(rn_selecionado)].copy()

# ── Segmentação Core / High End ────────────────────────────────────────────
df_core = df_rn[df_rn['BASE'] == 'CORE']
df_he   = df_rn[df_rn['BASE'] == 'HIGH END']

total_pdvs    = len(df_rn)
total_core    = len(df_core)
total_he      = len(df_he)
bateram_total = int(df_rn['BATEU_SCORE5'].sum())
bateram_core  = int(df_core['BATEU_SCORE5'].sum()) if not df_core.empty else 0
bateram_he    = int(df_he['BATEU_SCORE5'].sum())   if not df_he.empty  else 0
fora_meta     = total_pdvs - bateram_total
score5_pct    = (bateram_total / total_pdvs * 100)  if total_pdvs > 0 else 0.0

# ── KPIs OK média do RN ────────────────────────────────────────────────────
kpis_ok_media = df_rn['KPIs OK'].mean() if 'KPIs OK' in df_rn.columns else 0

# ─────────────────────────────────────────────────────────────────────────────
# PAINEL EXECUTIVO — CARDS DO TOPO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"### 📊 Painel Executivo — RN {rn_selecionado}")

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric("⭐ Score 5 (%)", f"{score5_pct:.1f}%",
              help="% de PDVs que atingiram os 5 KPIs")
with c2:
    st.metric("🏆 Score 5 (PDVs)", f"{bateram_total}",
              help="Quantidade de clientes com KPIs OK = 5")
with c3:
    st.metric("📍 PDVs na Rota", total_pdvs)
with c4:
    st.metric("🟡 Core (Total / ✅)", f"{total_core} / {bateram_core}")
with c5:
    st.metric("💎 High End (Total / ✅)", f"{total_he} / {bateram_he}")
with c6:
    st.metric("📊 KPIs Médios", f"{kpis_ok_media:.1f} / 5")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# BREAKDOWN POR KPI DO RN
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"#### 🎯 Atingimento por KPI — RN {rn_selecionado}")

kpi_cols = [k for k in KPIS if k in df_rn.columns]
if kpi_cols and total_pdvs > 0:
    kpi_data = []
    for k in kpi_cols:
        atingiram = int(df_rn[k].fillna(0).apply(lambda x: 1 if x == 1 else 0).sum())
        pct = atingiram / total_pdvs * 100
        kpi_data.append({"KPI": KPIS_LABELS.get(k, k), "Atingiram": atingiram,
                          "Total": total_pdvs, "% Atingimento": f"{pct:.0f}%"})
    df_kpi = pd.DataFrame(kpi_data)
    st.dataframe(df_kpi, use_container_width=True, hide_index=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TASK DE FATURAMENTO (META vs REAL)
# ─────────────────────────────────────────────────────────────────────────────
df_task = df_rn[df_rn.get('POSSUI TASK', pd.Series(dtype=str)) == 'S'] if 'POSSUI TASK' in df_rn.columns else pd.DataFrame()
if not df_task.empty and 'META TASK' in df_task.columns and 'REAL TASK' in df_task.columns:
    st.markdown(f"#### 📦 Task de Faturamento — RN {rn_selecionado}")
    meta_total = df_task['META TASK'].sum()
    real_total = df_task['REAL TASK'].sum()
    gap_task   = meta_total - real_total
    pct_task   = (real_total / meta_total * 100) if meta_total > 0 else 0

    t1, t2, t3, t4 = st.columns(4)
    with t1: st.metric("🎯 Meta Task (R\$)", f"R$ {meta_total:,.0f}")
    with t2: st.metric("✅ Real Task (R\$)", f"R$ {real_total:,.0f}")
    with t3: st.metric("❌ Gap Task (R\$)", f"R$ {gap_task:,.0f}")
    with t4: st.metric("📈 Atingimento Task", f"{pct_task:.1f}%")
    st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# MATRIZ DE CONSULTA POR CLIENTE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📋 Matriz de Clientes — Execução & KPIs Individuais")

busca = st.text_input("🔍 Filtrar por Nome do PDV ou Chave:", "")
mostrar_fora = st.checkbox("Mostrar apenas quem está FORA da meta", value=False)

df_exib = df_rn.copy()
if busca:
    df_exib = df_exib[
        df_exib['NOME PDV'].astype(str).str.contains(busca, case=False, na=False) |
        df_exib['CHAVE PDV'].astype(str).str.contains(busca, case=False, na=False)
    ]
if mostrar_fora:
    df_exib = df_exib[df_exib['BATEU_SCORE5'] == 0]

st.caption(f"Exibindo {len(df_exib)} de {total_pdvs} PDVs do RN {rn_selecionado}")

if df_exib.empty:
    st.info("Nenhum cliente encontrado com esse filtro.")
else:
    for _, row in df_exib.iterrows():
        base       = row.get('BASE', 'CORE')
        bateu      = row.get('BATEU_SCORE5', 0)
        kpis_ok    = int(row.get('KPIs OK', 0)) if pd.notna(row.get('KPIs OK')) else 0
        status_txt = f"✅ Score 5 completo ({kpis_ok}/5 KPIs)" if bateu == 1 else f"❌ Fora da meta ({kpis_ok}/5 KPIs)"
        icone      = "🟡" if base == 'CORE' else "💎"

        with st.expander(f"{icone} {row.get('NOME PDV', 'PDV')} — {status_txt}"):
            c1, c2, c3 = st.columns(3)

            with c1:
                st.write(f"**Chave PDV:** `{row.get('CHAVE PDV', '---')}`")
                st.write(f"**Segmento:** {icone} {base}")
                st.write(f"**Dia de Visita:** {row.get('VISITA', '---')}")
                st.write(f"**Operação:** {row.get('OPERAÇÃO', '---')}")
                st.write(f"**GV:** {row.get('GV', '---')}")

            with c2:
                st.write("**📋 KPIs:**")
                for k in kpi_cols:
                    val = row.get(k)
                    ok  = pd.notna(val) and val == 1
                    st.write(f"{'✅' if ok else '❌'} {KPIS_LABELS.get(k, k)}")

            with c3:
                # Task de Faturamento (se aplicável)
                if row.get('POSSUI TASK') == 'S':
                    meta_t = row.get('META TASK', 0)
                    real_t = row.get('REAL TASK', 0)
                    gap_t  = (meta_t - real_t) if pd.notna(meta_t) and pd.notna(real_t) else 0
                    pct_t  = (real_t / meta_t * 100) if pd.notna(meta_t) and meta_t > 0 else 0
                    st.write(f"**📦 Task Fat.:**")
                    st.write(f"Meta: `R$ {meta_t:,.0f}` | Real: `R$ {real_t:,.0f}`")
                    st.write(f"Gap: `R$ {gap_t:,.0f}` | `{pct_t:.1f}%`")
                else:
                    st.write("📦 Sem Task de Faturamento")

                # Tendências
                cerv = row.get('CERV (TEND)')
                he   = row.get('HE (TEND)')
                if pd.notna(cerv):
                    st.write(f"**🍺 Cerv. Tend.:** `{cerv:.1f}`")
                if pd.notna(he):
                    st.write(f"**🍾 HE Tend.:** `{he:.1f}`")
