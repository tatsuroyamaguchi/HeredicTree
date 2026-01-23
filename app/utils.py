import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import platform
import os
import pandas as pd
import logging

from parameter import FONT_FILES, SYSTEM_FONTS


def get_custom_fonts():
    """Load custom fonts from the fonts directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(base_dir, "fonts")
    
    registered_fonts = []
    
    for font_file in FONT_FILES:
        font_path = os.path.join(fonts_dir, font_file)
        
        if os.path.exists(font_path):
            try:
                fm.fontManager.addfont(font_path)
                prop = fm.FontProperties(fname=font_path)
                registered_fonts.append(prop.get_name())
            except Exception:
                pass
    
    return registered_fonts


def get_system_font():
    """Get system-specific Japanese font."""
    system = platform.system()
    font_path = SYSTEM_FONTS.get(system)
    
    if font_path and os.path.exists(font_path):
        try:
            return [fm.FontProperties(fname=font_path).get_name()]
        except Exception:
            pass
    
    return []


def configure_fonts():
    """
    Configure Matplotlib fonts for Japanese support with robust fallback.
    Priority: custom fonts > system Japanese fonts > DejaVu Sans > generic sans-serif
    """
    # Suppress font manager warnings
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    
    # Load custom fonts
    custom_fonts = get_custom_fonts()
    
    # Get system font
    system_fonts = get_system_font()
    
    # Combine font priorities
    final_fonts = custom_fonts + system_fonts + ['DejaVu Sans', 'sans-serif']
    
    # Apply font configuration
    plt.rcParams['font.family'] = final_fonts
    
    # PDF and Unicode stability settings
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['axes.unicode_minus'] = False


def parse_list_field(value):
    """Parse a comma-separated string into a list."""
    if pd.isna(value) or value == "":
        return []
    
    val_str = str(value)
    return [x.strip() for x in val_str.split(",") if x.strip()]


def parse_list_string(value, separator=","):
    """汎用的な文字列リスト解析"""
    if pd.isna(value) or value == "":
        return []
    val_str = str(value)
    # 全角カンマ対応などもここ一箇所で管理
    val_str = val_str.replace("、", separator) 
    # セミコロンやスペースの正規化もここで行う
    normalized = val_str.replace(";", separator).replace(" ", separator)
    return [x.strip() for x in normalized.split(separator) if x.strip()]


def parse_multiples_field(value):
    """
    Parse multiples field from string format to list of dictionaries.
    Format: "II-3+II-4:monozygotic;II-5+II-6:dizygotic"
    """
    if pd.isna(value) or str(value).strip() == "":
        return []
    
    multiples = []
    val_str = str(value).strip()
    
    for part in val_str.split(";"):
        if ":" not in part:
            continue
        
        ids_part, m_type = part.split(":", 1)
        ids = [i.strip() for i in ids_part.split("+") if i.strip()]
        
        if ids:
            multiples.append({
                "ids": ids,
                "type": m_type.strip()
            })
    
    return multiples


def normalize_boolean(value):
    """Normalize a value to boolean (True) or empty string."""
    if value is True or str(value).strip().lower() == 'true':
        return True
    return ""


def process_individuals(df_ind):
    """Process individuals dataframe into JSON format."""
    individuals = df_ind.to_dict(orient="records")
    # 変更点: "carrier" を追加
    bool_fields = ["proband", "client", "documented", "deceased", "pregnancy", "carrier", "donor", "surrogate"]
    
    for row in individuals:
        # Normalize boolean fields
        for field in bool_fields:
            row[field] = normalize_boolean(row.get(field))
    
    return individuals


def process_relationships(df_rel):
    """Process relationships dataframe into JSON format."""
    relationships = df_rel.to_dict(orient="records")
    
    for rel in relationships:
        # Handle consanguinity
        val = rel.get("consanguinity", False)
        if pd.isna(val) or val == "" or val is None:
            rel["consanguinity"] = False
        else:
            rel["consanguinity"] = bool(val)
        
        # Handle divorced field
        if "divorced" not in rel or pd.isna(rel["divorced"]):
            rel["divorced"] = ""
        
        # Parse list fields
        for field in ["children", "adopted_in", "adopted_out"]:
            rel[field] = parse_list_field(rel.get(field, ""))
        
        # Parse multiples field
        rel["multiples"] = parse_multiples_field(rel.get("multiples", ""))
    
    return relationships


def process_dataframe_for_json(df_ind, df_rel, current_meta, layout_config):
    """
    Convert DataFrames from DataEditor into JSON format.
    
    Args:
        df_ind: DataFrame of individuals
        df_rel: DataFrame of relationships
        current_meta: Metadata dictionary
        layout_config: Layout configuration dictionary
    
    Returns:
        Complete JSON dictionary for pedigree data
    """
    individuals = process_individuals(df_ind)
    relationships = process_relationships(df_rel)
    
    return {
        "meta": {"comments": current_meta.get("comments", "")},
        "layout": layout_config,
        "individual": individuals,
        "relationships": relationships
    }