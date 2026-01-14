import streamlit as st
import pandas as pd
import json
import io
import os
import copy
import shutil
import matplotlib as mpl

# Local imports
import json_data
from utils import configure_fonts, process_dataframe_for_json
from engine import PedigreeEngine
from drawer import draw_pedigree_chart
from dictionary import LANGUAGES
from pedigree_generator import generate_pedigree_data, parse_input_string


# ========================================
# Configuration and Initialization
# ========================================

def clear_matplotlib_cache():
    """Clear matplotlib cache directory."""
    cache_dir = mpl.get_cachedir()
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)


def initialize_session_state():
    """Initialize session state variables."""
    if 'lang' not in st.session_state:
        st.session_state.lang = "English"
    
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    
    if 'current_json' not in st.session_state:
        st.session_state.current_json = json_data.DEFAULT_JSON


def initialize_layout_defaults():
    """Initialize layout parameter defaults from current JSON."""
    current_layout = st.session_state.current_json.get("layout", {})
    
    defaults = {
        "ps_slider": float(current_layout.get("partner_spacing", 4.0)),
        "ms_slider": float(current_layout.get("min_sib_spacing", 2.0)),
        "gh_slider": float(current_layout.get("gen_height", 6.0)),
        "fg_slider": float(current_layout.get("family_gap", 1.0)),
        "uso_slider": float(current_layout.get("u_shape_offset", 3.0)),
        "ai_slider": int(current_layout.get("ajustment_iterations", 1)),
        "ss_slider": float(current_layout.get("symbol_size", 1.0)),
        "lw_slider": float(current_layout.get("line_width", 1.5)),
        "fs_slider": int(current_layout.get("font_size", 10)),
        "lo_slider": float(current_layout.get("label_offset", 0.5)),
        "lp_radio": current_layout.get("layout_priority", "Children to Parents (Top-down)")
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ========================================
# Data Loading Functions
# ========================================

def load_sample_data(data_content, success_message):
    """Load sample data into session state and update UI parameters."""
    st.session_state.current_json = data_content

    if "layout" in data_content:
        layout = data_content["layout"]
        st.session_state.ps_slider = float(layout.get("partner_spacing", 4.0))
        st.session_state.ms_slider = float(layout.get("min_sib_spacing", 2.0))
        st.session_state.gh_slider = float(layout.get("gen_height", 6.0))
        st.session_state.fg_slider = float(layout.get("family_gap", 1.0))
        st.session_state.uso_slider = float(layout.get("u_shape_offset", 3.0))
        st.session_state.ai_slider = int(layout.get("ajustment_iterations", 1))
        st.session_state.ss_slider = float(layout.get("symbol_size", 1.0))
        st.session_state.lw_slider = float(layout.get("line_width", 1.5))
        st.session_state.fs_slider = int(layout.get("font_size", 10))
        st.session_state.lo_slider = float(layout.get("label_offset", 0.5))
        st.session_state.lp_radio = layout.get("layout_priority", "Children to Parents (Top-down)")

    # Clear table cache
    for key in ['individual_df', 'rel_df']:
        if key in st.session_state:
            del st.session_state[key]
            
    st.sidebar.success(success_message)
    st.session_state.uploader_key += 1
    st.rerun()


# ========================================
# UI Component Functions
# ========================================

def render_language_toggle():
    """Render language toggle button in sidebar."""
    with st.sidebar:
        if st.button("🇬🇧 English / 🇯🇵 Japanese"):
            st.session_state.lang = "Japanese" if st.session_state.lang == "English" else "English"
            st.rerun()


def render_instructions(L):
    """Render instructions expander."""
    with st.expander("**How to Use**", expanded=False):
        st.markdown(L["how_to_use"])


def render_pedigree_generator(L):
    """Render the easy pedigree generator section."""
    with st.expander("**Easy Pedigree Generator**", expanded=False):
        info_text = ("家系の構成を入力するだけで、ベースとなる家系図を自動生成します。\n"
                    "詳細はEdit Data (Table View)で編集してください。") if st.session_state.lang == "Japanese" \
                    else "Generate a base Pedigree by simply entering the family structure.\nYou can edit the details in Edit Data (Table View)."
        st.info(info_text)
        
        g_col1, g_col2, g_col3 = st.columns(3)
        with g_col1:
            p_str = st.text_input(L["paternal"], value="M", help="M: Male, F: Female")
        with g_col2:
            m_str = st.text_input(L["maternal"], value="F")
        with g_col3:
            s_str = st.text_input(L["self_generation"], value="M")

        p_sibs = parse_input_string(p_str)
        m_sibs = parse_input_string(m_str)
        my_sibs = parse_input_string(s_str)

        g_col4, g_col5, g_col6 = st.columns(3)
        with g_col4:
            f_local_idx = st.number_input(L["father"], 1, max(1, len(p_sibs)), 1)
        with g_col5:
            m_local_idx = st.number_input(L["mother"], 1, max(1, len(m_sibs)), 1)
        with g_col6:
            s_idx = st.number_input(L["self"], 1, max(1, len(my_sibs)), 1)

        if st.button("Generate & Load Data", type="primary", use_container_width=True):
            if p_sibs and m_sibs and my_sibs:
                gen_data = generate_pedigree_data(
                    paternal_sibs=p_sibs,
                    maternal_sibs=m_sibs,
                    father_idx=f_local_idx,
                    mother_idx=len(p_sibs) + m_local_idx,
                    my_sibs=my_sibs,
                    self_idx=s_idx
                )
                load_sample_data(gen_data, "Generated successfully!")
            else:
                st.error("Please fill in all family members.")


def render_sidebar_data_loader(L):
    """Render sidebar data loading options."""
    # JSON Upload
    json_upload = st.sidebar.file_uploader(
        L["upload_label"], 
        type=["json"], 
        key=f"uploader_{st.session_state.uploader_key}"
    )
    
    # Load Reference
    if st.sidebar.button(L["load_ref"]):
        load_sample_data(json_data.REFERENCE_JSON, L["success_load"].format("Reference Pedigree"))
    
    # Load Example Files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    example_dir = os.path.join(current_dir, "examples")
    example_files = []
    if os.path.exists(example_dir):
        example_files = sorted([f for f in os.listdir(example_dir) if f.endswith(".json")])
    
    selected_example = st.sidebar.selectbox(L["sample_files"], options=["---"] + example_files)
    if st.sidebar.button(L["load_example"]):
        if selected_example != "---":
            example_path = os.path.join(example_dir, selected_example)
            try:
                with open(example_path, "r", encoding="utf-8") as f:
                    example_data = json.load(f)
                load_sample_data(example_data, L["success_load"].format(selected_example))
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
    
    # Process uploaded JSON
    if json_upload is not None:
        try:
            uploaded_data = json.load(json_upload)
            if "meta" not in uploaded_data:
                uploaded_data["meta"] = {"comments": ""}
            if "layout" not in uploaded_data:
                uploaded_data["layout"] = json_data.DEFAULT_JSON["layout"].copy()
            load_sample_data(uploaded_data, "Loaded JSON!")
        except Exception as e:
            st.sidebar.error(f"Error loading JSON: {e}")


def render_layout_settings(L):
    """Render layout settings in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.header(L["sidebar_layout_settings"])
    
    # Spacing Settings
    st.sidebar.subheader(L["sub_spacing"])
    partner_spacing = st.sidebar.number_input(L["label_ps"], 1.0, 20.0, step=0.5, key="ps_slider", help=L["help_ps"])
    min_sib_spacing = st.sidebar.number_input(L["label_ms"], 0.5, 20.0, step=0.5, key="ms_slider", help=L["help_ms"])
    gen_height = st.sidebar.number_input(L["label_gh"], 1.0, 30.0, step=0.5, key="gh_slider", help=L["help_gh"])
    family_gap = st.sidebar.number_input(L["label_fg"], -10.0, 30.0, step=0.5, key="fg_slider", help=L["help_fg"])
    u_shape_offset = st.sidebar.number_input(L["label_uso"], 0.5, 20.0, step=0.1, key="uso_slider", help=L["help_uso"])
    adjustment_iterations = st.sidebar.number_input(L["label_ai"], 1, 20, step=1, key="ai_slider", help=L["help_ai"])
    
    layout_priority_display = st.sidebar.radio(L["label_lp"], options=L["lp_options"], key="lp_radio_display", help=L["help_lp"])
    layout_priority = "Children to Parents (Top-down)" if layout_priority_display == L["lp_options"][0] else "Parents to Children (Bottom-up)"
    
    # Visual Settings
    st.sidebar.subheader(L["sub_visual"])
    symbol_size = st.sidebar.number_input(L["label_ss"], 0.1, 5.0, step=0.1, key="ss_slider", help=L["help_ss"])
    line_width = st.sidebar.number_input(L["label_lw"], 0.5, 5.0, step=0.1, key="lw_slider", help=L["help_lw"])
    font_size = st.sidebar.number_input(L["label_fs"], 5, 20, step=1, key="fs_slider", help=L["help_fs"])
    label_offset = st.sidebar.number_input(L["label_lo"], 0.0, 2.0, step=0.1, key="lo_slider", help=L["help_lo"])
    
    return {
        'partner_spacing': partner_spacing,
        'min_sib_spacing': min_sib_spacing,
        'gen_height': gen_height,
        'family_gap': family_gap,
        'u_shape_offset': u_shape_offset,
        'adjustment_iterations': adjustment_iterations,
        'layout_priority': layout_priority,
        'symbol_size': symbol_size,
        'line_width': line_width,
        'font_size': font_size,
        'label_offset': label_offset,
        'node_width': 1,
    }


def prepare_individual_dataframe():
    """Prepare individual dataframe from JSON data."""
    df_ind = pd.DataFrame(st.session_state.current_json.get("individual", []))
    
    str_cols = ["id", "gender", "affected", "label"]
    bool_cols = ["proband", "client", "documented", "deceased", "pregnancy"]
    
    # Clean string columns
    for col in str_cols:
        if col not in df_ind.columns:
            df_ind[col] = ""
        else:
            df_ind[col] = df_ind[col].astype(str).replace("nan", "")
    
    # Initialize boolean columns
    for col in bool_cols:
        if col not in df_ind.columns:
            df_ind[col] = False
        else:
            df_ind[col] = df_ind[col].map(
                lambda x: True if str(x).strip().lower() == 'true' or x is True else False
            )
            df_ind[col] = df_ind[col].astype(bool)
    
    return df_ind[str_cols + bool_cols].copy()


def prepare_relationships_dataframe():
    """Prepare relationships dataframe from JSON data."""
    rel_list = copy.deepcopy(st.session_state.current_json.get("relationships", []))
    processed_rels = []
    
    for r in rel_list:
        if "divorced" not in r:
            r["divorced"] = ""
        
        r["children"] = ",".join(r.get("children", []))
        
        if "multiples" in r and isinstance(r["multiples"], list):
            m_parts = [f"{'+'.join(m.get('ids', []))}:{m.get('type', 'dizygotic')}" 
                      for m in r["multiples"]]
            r["multiples"] = ";".join(m_parts)
        else:
            r["multiples"] = ""
        
        r["adopted_in"] = ",".join(r.get("adopted_in", [])) if isinstance(r.get("adopted_in"), list) else r.get("adopted_in", "")
        r["adopted_out"] = ",".join(r.get("adopted_out", [])) if isinstance(r.get("adopted_out"), list) else r.get("adopted_out", "")
        
        processed_rels.append(r)
    
    df_rel = pd.DataFrame(processed_rels)
    
    # Initialize consanguinity column
    if "consanguinity" not in df_rel.columns:
        df_rel["consanguinity"] = False
    else:
        df_rel["consanguinity"] = df_rel["consanguinity"].astype('string').fillna(False)
        df_rel["consanguinity"] = df_rel["consanguinity"].map(
            lambda x: True if str(x).strip().lower() == 'true' or x is True else False
        )
        df_rel["consanguinity"] = df_rel["consanguinity"].astype(bool)
    
    return df_rel


def render_data_editor():
    """Render data editor section."""
    with st.expander("Edit Data (Table View)", expanded=False):
        # Initialize dataframes if needed
        if 'individual_df' not in st.session_state:
            st.session_state.individual_df = prepare_individual_dataframe()
        
        if 'rel_df' not in st.session_state:
            st.session_state.rel_df = prepare_relationships_dataframe()
        
        # Individuals table
        st.subheader("Individuals")
        edited_ind = st.data_editor(
            st.session_state.individual_df,
            num_rows="dynamic",
            column_config={
                "gender": st.column_config.TextColumn("gender", default=""),
                "affected": st.column_config.TextColumn("affected", default=""),
                "label": st.column_config.TextColumn("label", default=""),
                "deceased": st.column_config.CheckboxColumn("deceased", default=False),
                "proband": st.column_config.CheckboxColumn("proband", default=False),
                "client": st.column_config.CheckboxColumn("client", default=False),
                "documented": st.column_config.CheckboxColumn("documented", default=False),
                "pregnancy": st.column_config.CheckboxColumn("pregnancy", default=False),
            }
        )
        
        # Relationships table
        st.subheader("Relationships")
        edited_rel = st.data_editor(
            st.session_state.rel_df,
            num_rows="dynamic",
            column_config={
                "consanguinity": st.column_config.CheckboxColumn("consanguinity", default=False),
            }
        )
        
        # Metadata
        st.markdown("---")
        st.subheader("Metadata / Comments")
        current_meta = st.session_state.current_json.get("meta", {})
        comments = st.text_area("Comments", value=current_meta.get("comments", ""), height=200)
        current_meta["comments"] = comments
        
        return edited_ind, edited_rel, current_meta


def render_pedigree_output(positioned_nodes, relationships, live_config, latest_json_data):
    """Render pedigree chart and download options."""
    st.subheader("Pedigree Chart")
    fig = draw_pedigree_chart(
        positioned_nodes,
        relationships,
        live_config,
        meta=latest_json_data["meta"]
    )
    st.pyplot(fig)
    
    # Download options
    st.markdown("### Download Options")
    formats = [
        {"label": "SVG", "ext": "svg", "mime": "image/svg+xml"},
        {"label": "PNG", "ext": "png", "mime": "image/png"},
        {"label": "JPEG", "ext": "jpg", "mime": "image/jpeg"},
        {"label": "TIFF", "ext": "tiff", "mime": "image/tiff"},
        {"label": "PDF", "ext": "pdf", "mime": "application/pdf"},
    ]
    
    for fmt in formats:
        col1, col2 = st.columns([1, 8])
        with col1:
            buf = io.BytesIO()
            if fmt["ext"] in ["svg", "tiff", "pdf"]:
                fig.savefig(buf, format=fmt["ext"], bbox_inches='tight')
            else:
                fig.savefig(buf, format=fmt["ext"], bbox_inches='tight', dpi=300)
            buf.seek(0)
            st.download_button(
                label=f"**{fmt['label']}**",
                data=buf,
                file_name=f"pedigree_chart.{fmt['ext']}",
                mime=fmt["mime"],
                use_container_width=True
            )
    
    # JSON download
    st.markdown("---")
    json_str = json.dumps(latest_json_data, indent=2)
    st.download_button(
        "**Download JSON**",
        json_str,
        file_name="pedigree_data.json",
        mime="application/json"
    )


def render_readme():
    """Render README section."""
    st.markdown("---")
    with st.expander("README", expanded=False):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        readme_paths = [
            os.path.join(current_dir, "README.md"),
            os.path.join(current_dir, "..", "README.md")
        ]
        
        readme_content = ""
        for path in readme_paths:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                break
        
        if readme_content:
            st.markdown("---")
            st.markdown(readme_content)
        else:
            st.sidebar.warning("README.md not found.")


# ========================================
# Main Application
# ========================================

def main():
    """Main application entry point."""
    # Initial setup
    clear_matplotlib_cache()
    configure_fonts()
    st.set_page_config(
        page_title="HeredicTree",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Language toggle
    render_language_toggle()
    L = LANGUAGES[st.session_state.lang]
    
    # Title
    st.title(L["title"])
    
    # UI Sections
    render_instructions(L)
    render_pedigree_generator(L)
    render_sidebar_data_loader(L)
    
    # Layout settings
    initialize_layout_defaults()
    live_config = render_layout_settings(L)
    
    # Data editor
    edited_ind, edited_rel, current_meta = render_data_editor()
    
    # Process and render
    latest_json_data = process_dataframe_for_json(edited_ind, edited_rel, current_meta, live_config)
    
    if latest_json_data:
        # Calculate layout
        engine = PedigreeEngine(latest_json_data, live_config)
        positioned_nodes = engine.calculate_layout(
            adjustment_iterations=live_config['adjustment_iterations'],
            priority=live_config['layout_priority']
        )
        
        # Render output
        render_pedigree_output(
            positioned_nodes,
            latest_json_data["relationships"],
            live_config,
            latest_json_data
        )
    
    # README
    render_readme()


if __name__ == "__main__":
    main()