import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import platform
import os
import pandas as pd
import logging

def configure_fonts():
    """Matplotlib のフォント設定（Unicode・多言語対応）"""
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

    # --- 1. フォントファイルの直接登録 (./fonts/ フォルダ) ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_files = [
        "NotoSans-Regular.ttf",
        "NotoSansJP-Regular.ttf",
        "NotoSansKR-Regular.ttf",
        "NotoSansSC-Regular.ttf",
        "NotoSansTC-Regular.ttf",
    ]

    for f_name in font_files:
        path = os.path.join(base_dir, "fonts", f_name)
        if os.path.exists(path):
            try:
                fm.fontManager.addfont(path)
            except Exception:
                pass

    # --- 2. Unicode / PDF 安定化設定 ---
    plt.rcParams['pdf.fonttype'] = 42           # TrueType 埋め込み
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['axes.unicode_minus'] = False  # マイナス記号の文字化け防止

    # --- 3. フォントファミリーの優先順位設定 ---
    # ここに記述した順番でフォントが探索されます
    plt.rcParams['font.family'] = [
        'Noto Sans JP', 'Noto Sans KR', 'Noto Sans SC', 'Noto Sans TC', 'Noto Sans',
        'Hiragino Sans', 'Yu Gothic', 'MS Gothic', 'DejaVu Sans', 'sans-serif'
    ]


def process_dataframe_for_json(df_ind, df_rel, current_meta, layout_config):
    """DataEditorから取得したDataFrameをJSON形式（辞書）に変換する"""
    final_ind = df_ind.to_dict(orient="records")
    bool_fields = ["proband", "client", "documented", "deceased", "pregnancy"]
    for row in final_ind:
        for field in bool_fields:
            val = row.get(field)
            # True 以外（False, None, NaN）はすべて空文字にする
            if val is True or str(val).lower() == 'true':
                row[field] = True
            else:
                row[field] = ""
                
    final_rel = df_rel.to_dict(orient="records")
    for r in final_rel:
        val = r.get("consanguinity", False)
        if pd.isna(val) or val == "" or val is None:
            r["consanguinity"] = False
        else:
            r["consanguinity"] = bool(val)
        
        # Divorced handling
        if "divorced" not in r or pd.isna(r["divorced"]):
            r["divorced"] = ""

        # List conversions
        for l_col in ["children", "adopted_in", "adopted_out"]:
            val = str(r.get(l_col, "")) if not pd.isna(r.get(l_col)) else ""
            r[l_col] = [x.strip() for x in val.split(",") if x.strip()]
        
        # Multiples handling
        m_str = str(r.get("multiples", "")) if not pd.isna(r.get("multiples")) else ""
        new_mults = []
        if m_str.strip():
            for part in m_str.split(";"):
                if ":" in part:
                    ids_part, m_type = part.split(":", 1)
                    new_mults.append({
                        "ids": [i.strip() for i in ids_part.split("+") if i.strip()],
                        "type": m_type.strip()
                    })
        r["multiples"] = new_mults

    return {
        "meta": {"comments": current_meta.get("comments", "")},
        "layout": layout_config,
        "individual": final_ind,
        "relationships": final_rel
    }
