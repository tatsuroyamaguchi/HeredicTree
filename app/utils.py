import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import platform
import os
import pandas as pd
import logging

def configure_fonts():
    """Matplotlib のフォント設定（日本語対応 + 確実なフォールバック）"""

    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

    # --- 1. カスタムフォントの読み込み ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    custom_font_paths = [
        os.path.join(base_dir, "fonts", "NotoSansJP-Regular.ttf"),
        os.path.join(base_dir, "fonts", "NotoSans-Regular.ttf"),
        os.path.join(base_dir, "fonts", "NotoSansKR-Regular.ttf"),
        os.path.join(base_dir, "fonts", "NotoSansSC-Regular.ttf"),
        os.path.join(base_dir, "fonts", "NotoSansTC-Regular.ttf"),
    ]

    registered_fonts = []

    for path in custom_font_paths:
        if os.path.exists(path):
            try:
                fm.fontManager.addfont(path)
                prop = fm.FontProperties(fname=path)
                registered_fonts.append(prop.get_name())
            except Exception:
                pass

    # --- 2. OS に応じた標準日本語フォント ---
    system = platform.system()

    fallback_fonts = []

    if system == "Darwin":  # macOS
        mac_font = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
        if os.path.exists(mac_font):
            fallback_fonts.append(fm.FontProperties(fname=mac_font).get_name())

    elif system == "Windows":
        win_font = "C:/Windows/Fonts/msgothic.ttc"
        if os.path.exists(win_font):
            fallback_fonts.append(fm.FontProperties(fname=win_font).get_name())

    else:  # Linux
        linux_font = "/usr/share/fonts/truetype/ipafont-gothic/ipagp.ttf"
        if os.path.exists(linux_font):
            fallback_fonts.append(fm.FontProperties(fname=linux_font).get_name())

    # --- 3. 最終フォント優先順の設定 ---
    # custom > fallback Japanese > DejaVu Sans > generic sans-serif
    final_fonts = registered_fonts + fallback_fonts + ['DejaVu Sans', 'sans-serif']

    plt.rcParams['font.family'] = final_fonts

    # --- 4. PDF / Unicode 安定化 ---
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['axes.unicode_minus'] = False


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