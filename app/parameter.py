# Constants
UPLOADER_KEY = 'uploader_key'
CURRENT_JSON_KEY = 'current_json'
LANG_KEY = 'lang'
DEFAULT_LANG = "English"

# Layout parameter keys
LAYOUT_PARAMS = {
    'ps_slider': ('partner_spacing', 4.0, float),
    'ms_slider': ('min_sib_spacing', 2.0, float),
    'gh_slider': ('gen_height', 6.0, float),
    'fg_slider': ('family_gap', 1.0, float),
    'uso_slider': ('u_shape_offset', 3.0, float),
    'ai_slider': ('adjustment_iterations', 1, int),
    'ss_slider': ('symbol_size', 1.0, float),
    'lw_slider': ('line_width', 1.5, float),
    'fs_slider': ('font_size', 10, int),
    'lo_slider': ('label_offset', 0.5, float),
    'lp_radio': ('layout_priority', "Children to Parents (Top-down)", str),
}

# Roman numeral mapping for generation parsing
ROMAN_TO_INT = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
    "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15
}

INT_TO_ROMAN = {v: k for k, v in ROMAN_TO_INT.items()}

# Default layout configuration
DEFAULT_LAYOUT = {
    "partner_spacing": 1.5,
    "min_sib_spacing": 2.0,
    "gen_height": 4.0,
    "family_gap": 1.0,
    "u_shape_offset": 2.0,
    "adjustment_iterations": 1,
    "layout_priority": "Children to Parents (Top-down)",
    "symbol_size": 1.0,
    "line_width": 1.5,
    "font_size": 10,
    "label_offset": 0.2,
    "node_width": 1
}

# Generation labels
GENERATION_LABELS = {
    1: "Paternal GF",
    2: "Paternal GM",
    3: "Maternal GF",
    4: "Maternal GM"
}


# Font file names
FONT_FILES = [
    "NotoSansJP-Regular.ttf",
    "NotoSans-Regular.ttf",
    "NotoSansKR-Regular.ttf",
    "NotoSansSC-Regular.ttf",
    "NotoSansTC-Regular.ttf",
]

# System font paths by OS
SYSTEM_FONTS = {
    "Darwin": "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",  # macOS
    "Windows": "C:/Windows/Fonts/msgothic.ttc",
    "Linux": "/usr/share/fonts/truetype/ipafont-gothic/ipagp.ttf"
}


# Constants
ROMANS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 
          6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}

GENDER_SHAPES = {
    "M": "square",
    "F": "circle",
    "A": "triangle",
    "N": "diamond",
    "U": "diamond",
    "non-binary": "diamond",
    "I": "infertility",
    "NC": "no_children"
}

AFFECTED_COLORS = {
    "A2-1": "black",
    "A2-2": "#999999",
    "A4-1": "black",
    "A4-2": "#444444",
    "A4-3": "#999999",
    "A4-4": "#CCCCCC"
}

