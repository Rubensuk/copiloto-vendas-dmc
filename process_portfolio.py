import os
import sys
import pandas as pd
import numpy as np
import json
import argparse

class PortfolioEngine:
    """
    Motor de Engenharia e Análise de Dados para a Revenda DMC em Araguaína/TO.
    Processa a planilha PlanificPortfolio.xlsx.xls (Aba 'Export').
    """

    def __init__(self, filepath="PlanificPortfolio.xlsx.xls"):
        self.filepath = filepath
        self.data = {}
        self.summary = {}

        # Colunas oficiais de marcas por categoria
        self.real_600_cols = ['SPT 600', 'STL 600', 'STL PG 600', 'BUD 600', 'COR 600', 'ORI 600 ', 'OUTROS 600']
        self.real_ln_cols = ['COR LN', 'STL LN', 'STL PG LN', 'SPT LN', 'MIC LN', 'OUTROS LN']

    def load_and_process(self, custom_path=None):
        target_path = custom_path or self.filepath
        if not os.path.exists(target_path):
            for ext in ['.xlsx', '.xls', '.xlsx.xls', '.csv']:
                base = os.path.splitext(target_path)[0]
                if os.path.exists(base + ext):
                    target_path = base + ext
                    break

        if not os.path.exists(target_path):
            print(f"[Aviso] Arquivo '{target_path}' não encontrado localmente.")
            return False

        try:
            # Tenta carregar a aba Export ou primeira aba
            excel_file = pd.ExcelFile(target_path)
            sheet_name = 'Export' if 'Export' in excel_file.sheet_names else excel_file.sheet_names[0]
            df = pd.read_excel(target_path, sheet_name=sheet_name)
            
            # Normalização de nomes de colunas
            df.columns = [str(c).strip() for c in df.columns]

            # Tratamentos de Realizado e Falta (Gap)
            cols_600_presentes = [c for c in self.real_600_cols if c in df.columns]
            cols_ln_presentes = [c for c in self.real_ln_cols if c in df.columns]

            df['REAL_600'] = df[cols_600_presentes].sum(axis=1) if cols_600_presentes else 0
            df['REAL_LN'] = df[cols_ln_presentes].sum(axis=1) if cols_ln_presentes else 0

            meta_600_col = '600' if '600' in df.columns else 'META_600'
            meta_ln_col = 'LN' if 'LN' in df.columns else 'META_LN'

            df['FALTA_600'] = df.apply(
                lambda r: max(0, float(r[meta_600_col]) - float(r['REAL_600'])) if meta_600_col in df.columns and pd.notna(r[meta_600_col]) else 0,
                axis=1
            )

            df['FALTA_LN'] = df.apply(
                lambda r: max(0, float(r[meta_ln_col]) - float(r['REAL_LN'])) if meta_ln_col in df.columns and pd.notna(r[meta_ln_col]) else 0,
                axis=1
            )

            # Extrai lista de RNs disponíveis
            rns_disponiveis = sorted([int(x) for x in df['RN'].dropna().unique()]) if 'RN' in df.columns else []

            for rn in rns_disponiveis:
                df_rn = df[df['RN'] == rn]
                self.data[rn] = self._process_rn_dataframe(df_rn, rn)

            self._consolidate_revenda(rns_disponiveis)
            return True

        except Exception as e:
            print(f"[Erro] Falha ao processar planilha: {str(e)}")
            return False

    def _process_rn_dataframe(self, df, rn):
        pdvs = []
        for _, row in df.iterrows():
            base_segmento = str(row.get('BASE', row.get('SEGMENTO', 'CORE'))).upper()
            bateu_meta = int(row.get('BATEU META', 0)) if pd.notna(row.get('BATEU META')) else 0

            pdvs.append({
                'rn': rn,
                'chave_pdv': str(row.get('CHAVE PDV', row.get('COD_PDV', ''))),
                'nome_pdv': str(row.get('NOME PDV', row.get('CLIENTE', ''))),
                'visita': str(row.get('VISITA', '---')),
                'base': base_segmento,
                'operacao': str(row.get('OPERAÇÃO', '---')),
                'meta_inteira': float(row.get('INTEIRA', 0) or 0),
                'meta_rgb': float(row.get('RGB', 0) or 0),
                'meta_600': float(row.get('600', 0) or 0),
                'real_600': float(row.get('REAL_600', 0) or 0),
                'falta_600': float(row.get('FALTA_600', 0) or 0),
                'meta_ln': float(row.get('LN', 0) or 0),
                'real_ln': float(row.get('REAL_LN', 0) or 0),
                'falta_ln': float(row.get('FALTA_LN', 0) or 0),
                'bateu_meta': bateu_meta
            })
        return pdvs

    def _consolidate_revenda(self, rns):
        totais_revenda = {'total_pdvs': 0, 'pdvs_meta': 0, 'score_5_pct': 0.0}

        for rn in rns:
            pdvs = self.data.get(rn, [])
            total_pdvs = len(pdvs)
            bateram_meta = sum(p['bateu_meta'] for p in pdvs)
            pct = (bateram_meta / total_pdvs * 100) if total_pdvs > 0 else 0.0

            self.summary[rn] = {
                'total_pdvs': total_pdvs,
                'bateram_meta': bateram_meta,
                'fora_meta': total_pdvs - bateram_meta,
                'score_5_pct': round(pct, 1),
                'falta_600_total': sum(p.get('falta_600', 0) for p in pdvs if p['base'] == 'HIGH END'),
                'falta_ln_total': sum(p.get('falta_ln', 0) for p in pdvs if p['base'] == 'HIGH END')
            }

            totais_revenda['total_pdvs'] += total_pdvs
            totais_revenda['pdvs_meta'] += bateram_meta

        tot_pdvs = totais_revenda['total_pdvs']
        tot_meta = totais_revenda['pdvs_meta']
        totais_revenda['score_5_pct'] = round((tot_meta / tot_pdvs * 100), 1) if tot_pdvs > 0 else 0.0
        self.summary['REVENDA_TOTAL'] = totais_revenda

    def generate_rn_report(self, rn):
        rn = int(rn)
        pdvs = self.data.get(rn, [])
        info = self.summary.get(rn, {})

        report = [
            f"============================================================",
            f"📊 PAINEL EXECUTIVO - ROTEIRO RN {rn} | ARAGUAÍNA/TO",
            f"============================================================",
            f"⭐ Score 5 (Atingimento Geral): {info.get('score_5_pct', 0.0)}%",
            f"📍 Total de PDVs na Rota: {info.get('total_pdvs', 0)}",
            f"✅ Bateram Meta: {info.get('bateram_meta', 0)} PDVs",
            f"❌ Fora da Meta: {info.get('fora_meta', 0)} PDVs",
            f"------------------------------------------------------------",
            f"📋 MATRIZ DE GAPS & EXECUÇÃO (HIGH END):",
            f"• Falta Total 600ml: {info.get('falta_600_total', 0)} SKUs",
            f"• Falta Total Long Necks: {info.get('falta_ln_total', 0)} SKUs",
            f"============================================================"
        ]

        return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="PlanificPortfolio.xlsx.xls")
    parser.add_argument("--rn", type=int)
    args = parser.parse_args()

    engine = PortfolioEngine(filepath=args.file)
    success = engine.load_and_process()

    if success:
        if args.rn:
            print(engine.generate_rn_report(args.rn))
        else:
            print(json.dumps(engine.summary, indent=2, ensure_ascii=False))
