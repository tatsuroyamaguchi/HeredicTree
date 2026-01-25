import streamlit as st
import pandas as pd
import json
import io
import os
import shutil
import matplotlib as mpl

# Local imports
from utils import configure_fonts, process_dataframe_for_json, prepare_individual_dataframe, prepare_relationships_dataframe
from engine import PedigreeEngine
from drawer import draw_pedigree_chart
from translation import LANGUAGES
from pedigree_generator import generate_pedigree_data, parse_input_string
from parameter import UPLOADER_KEY, CURRENT_JSON_KEY, LANG_KEY, DEFAULT_LANG, LAYOUT_PARAMS, DEFAULT_LAYOUT
from instructions import render_instructions

# ========================================
# Configuration and Initialization
# ========================================

def clear_matplotlib_cache():
    """Clear matplotlib cache directory."""
    cache_dir = mpl.get_cachedir()
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)


def initialize_session_state():
    """Initialize session state variables."""
    fallback_json = {
        "meta": {"comments": ""},
        "layout": DEFAULT_LAYOUT,
        "individual": [],
        "relationships": []
    }

    initial_json = fallback_json
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        example_path = os.path.join(current_dir, "examples", "1. Simple_Pedigree.json")
        
        if os.path.exists(example_path):
            with open(example_path, "r", encoding="utf-8") as f:
                initial_json = json.load(f)
    except Exception:
        pass

    defaults = {
        LANG_KEY: DEFAULT_LANG,
        UPLOADER_KEY: 0,
        CURRENT_JSON_KEY: initial_json
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def initialize_layout_defaults():
    """Initialize layout parameter defaults from current JSON."""
    current_layout = st.session_state[CURRENT_JSON_KEY].get("layout", {})
    
    for key, (layout_key, default, converter) in LAYOUT_PARAMS.items():
        if key not in st.session_state:
            st.session_state[key] = converter(current_layout.get(layout_key, default))


# ========================================
# Data Loading Functions
# ========================================

def update_layout_params_from_json(data_content):
    """Update layout parameters in session state from JSON data."""
    layout = data_content.get("layout", {})
    
    for key, (layout_key, default, converter) in LAYOUT_PARAMS.items():
        st.session_state[key] = converter(layout.get(layout_key, default))


def clear_table_cache():
    """Clear cached table data from session state."""
    cache_keys = ['individual_df', 'rel_df']
    for key in cache_keys:
        if key in st.session_state:
            del st.session_state[key]


def load_sample_data(data_content, success_message):
    """Load sample data into session state and update UI parameters."""
    st.session_state[CURRENT_JSON_KEY] = data_content
    
    if "layout" in data_content:
        update_layout_params_from_json(data_content)
    
    clear_table_cache()
    st.sidebar.success(success_message)
    st.session_state[UPLOADER_KEY] += 1
    st.rerun()


# ========================================
# UI Component Functions
# ========================================

def render_language_toggle(L):
    """Render language toggle button with current language indicator."""
    langs = ["English", "Japanese", "Español", "Deutsch"]
    if st.button("Change Language (EN/JP/ES/DE): " + L["language"], use_container_width=False):
        current_lang = st.session_state.get(LANG_KEY, "English")
        try:
            current_idx = langs.index(current_lang)
        except ValueError:
            current_idx = 0
            
        next_idx = (current_idx + 1) % len(langs)
        st.session_state[LANG_KEY] = langs[next_idx]
        st.rerun()


def render_pedigree_generator(L):
    """Render the easy pedigree generator section."""
    with st.expander("**Easy Pedigree Generator**", expanded=False):
        info_text = L["easy_pedigree_generator"]
        st.info(info_text)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            p_str = st.text_input(L["paternal"], value="M", help="M: Male, F: Female")
        with col2:
            m_str = st.text_input(L["maternal"], value="F")
        with col3:
            s_str = st.text_input(L["self_generation"], value="M")
        
        p_sibs = parse_input_string(p_str)
        m_sibs = parse_input_string(m_str)
        my_sibs = parse_input_string(s_str)
        
        col4, col5, col6 = st.columns(3)
        with col4:
            f_local_idx = st.number_input(L["father"], 1, max(1, len(p_sibs)), 1)
        with col5:
            m_local_idx = st.number_input(L["mother"], 1, max(1, len(m_sibs)), 1)
        with col6:
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
    json_upload = st.sidebar.file_uploader(
        L["upload_label"],
        type=["json"],
        key=f"uploader_{st.session_state[UPLOADER_KEY]}"
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    example_dir = os.path.join(current_dir, "examples")
    example_files = []
    
    if os.path.exists(example_dir):
        example_files = sorted([
            f for f in os.listdir(example_dir) if f.endswith(".json")
        ])
    
    selected_example = st.sidebar.selectbox(
        L["sample_files"],
        options=["---"] + example_files
    )
    
    if selected_example != "---":
        example_path = os.path.join(example_dir, selected_example)
        if os.path.exists(example_path):
            with open(example_path, "r", encoding="utf-8") as f:
                example_content = f.read()
            
            st.sidebar.download_button(
                label=f"Download {selected_example}",
                data=example_content,
                file_name=selected_example,
                mime="application/json"
            )
    
    if json_upload is not None:
        try:
            uploaded_data = json.load(json_upload)
            if "meta" not in uploaded_data:
                uploaded_data["meta"] = {"comments": ""}
            if "layout" not in uploaded_data:
                uploaded_data["layout"] = DEFAULT_LAYOUT.copy()
            load_sample_data(uploaded_data, "Loaded JSON!")
        except Exception as e:
            st.sidebar.error(f"Error loading JSON: {e}")


def render_layout_settings(L):
    """Render layout settings in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.header(L["sidebar_layout_settings"])
    
    st.sidebar.subheader(L["sub_spacing"])
    
    spacing_inputs = {
        'partner_spacing': st.sidebar.number_input(L["label_ps"], 1.0, 20.0, step=0.5, key="ps_slider", help=L["help_ps"]),
        'min_sib_spacing': st.sidebar.number_input(L["label_ms"], 0.5, 20.0, step=0.5, key="ms_slider", help=L["help_ms"]),
        'gen_height': st.sidebar.number_input(L["label_gh"], 1.0, 30.0, step=0.5, key="gh_slider", help=L["help_gh"]),
        'family_gap': st.sidebar.number_input(L["label_fg"], -10.0, 30.0, step=0.5, key="fg_slider", help=L["help_fg"]),
        'u_shape_offset': st.sidebar.number_input(L["label_uso"], 0.5, 20.0, step=0.1, key="uso_slider", help=L["help_uso"]),
        'adjustment_iterations': st.sidebar.number_input(L["label_ai"], 1, 20, step=1, key="ai_slider", help=L["help_ai"]),
    }
    
    layout_priority_display = st.sidebar.radio(
        L["label_lp"], options=L["lp_options"], key="lp_radio_display", help=L["help_lp"]
    )
    
    layout_priority = (
        "Children to Parents (Top-down)" if layout_priority_display == L["lp_options"][0] else "Parents to Children (Bottom-up)"
    )
    
    st.sidebar.subheader(L["sub_visual"])
    
    visual_inputs = {
        'symbol_size': st.sidebar.number_input(L["label_ss"], 0.1, 5.0, step=0.1, key="ss_slider", help=L["help_ss"]),
        'line_width': st.sidebar.number_input(L["label_lw"], 0.5, 5.0, step=0.1, key="lw_slider", help=L["help_lw"]),
        'label_offset': st.sidebar.number_input(L["label_lo"], 0.0, 2.0, step=0.1, key="lo_slider", help=L["help_lo"]),
        'font_size': st.sidebar.number_input(L["label_fs"], 5, 20, step=1, key="fs_slider", help=L["help_fs"]),
        'arrow_size': st.sidebar.number_input(L["label_as"], 5, 30, step=1, key="as_slider", help=L["help_as"]),
        'proband_size': st.sidebar.number_input(L["label_pbs"], 5, 30, step=1, key="pbs_slider", help=L["help_pbs"]),
    }
    
    config = {
        **spacing_inputs,
        **visual_inputs,
        'layout_priority': layout_priority,
        'node_width': 1,
    }
    
    return config


def render_data_editor():
    """Render data editor section."""
    with st.expander("Edit Data (Table View)", expanded=False):
        # Initialize dataframes if needed using utils function
        if 'individual_df' not in st.session_state:
            st.session_state.individual_df = prepare_individual_dataframe(
                st.session_state[CURRENT_JSON_KEY]
            )
        
        if 'rel_df' not in st.session_state:
            st.session_state.rel_df = prepare_relationships_dataframe(
                st.session_state[CURRENT_JSON_KEY]
            )
        
        st.subheader("Individuals")
        edited_ind = st.data_editor(
            st.session_state.individual_df,
            num_rows="dynamic",
            column_config={
                "gender": st.column_config.TextColumn("gender", default=""),
                "affected": st.column_config.TextColumn("affected", default=""),
                "label": st.column_config.TextColumn("label", default=""),
                "note_idv": st.column_config.TextColumn("note for individuals", default="", help="Internal note/memo. Not displayed in the chart.", width="medium"),
                "deceased": st.column_config.CheckboxColumn("deceased", default=False),
                "proband": st.column_config.CheckboxColumn("proband", default=False),
                "client": st.column_config.CheckboxColumn("client", default=False),
                "documented": st.column_config.CheckboxColumn("documented", default=False),
                "pregnancy": st.column_config.CheckboxColumn("pregnancy", default=False),
                "carrier": st.column_config.CheckboxColumn("carrier", default=False),
                "donor": st.column_config.CheckboxColumn("donor", default=False),
                "surrogate": st.column_config.CheckboxColumn("surrogate", default=False),
            }
        )
        
        st.subheader("Relationships")
        edited_rel = st.data_editor(
            st.session_state.rel_df,
            num_rows="dynamic",
            column_config={
                "consanguinity": st.column_config.CheckboxColumn(
                    "consanguinity", default=False
                ),
                "note_rel": st.column_config.TextColumn(
                    "note for relationships", default="", help="Internal note for relationship.", width="medium"
                ),
            }
        )
        
        st.markdown("---")
        st.subheader("Metadata / Comments")
        current_meta = st.session_state[CURRENT_JSON_KEY].get("meta", {})
        comments = st.text_area(
            "Comments",
            value=current_meta.get("comments", ""),
            height=200
        )
        current_meta["comments"] = comments
        
        return edited_ind, edited_rel, current_meta


def create_download_button(fig, format_info):
    """Create a download button for a specific format."""
    buf = io.BytesIO()
    
    if format_info["ext"] in ["svg", "tiff", "pdf"]:
        fig.savefig(buf, format=format_info["ext"], bbox_inches='tight')
    else:
        fig.savefig(buf, format=format_info["ext"], bbox_inches='tight', dpi=300)
    
    buf.seek(0)
    
    st.download_button(
        label=f"**{format_info['label']}**",
        data=buf,
        file_name=f"pedigree_chart.{format_info['ext']}",
        mime=format_info["mime"],
        use_container_width=True
    )


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
    
    st.markdown("### Download Options")
    
    formats = [
        {"label": "SVG", "ext": "svg", "mime": "image/svg+xml"},
        {"label": "PNG", "ext": "png", "mime": "image/png"},
        {"label": "JPEG", "ext": "jpg", "mime": "image/jpeg"},
        {"label": "TIFF", "ext": "tiff", "mime": "image/tiff"},
        {"label": "PDF", "ext": "pdf", "mime": "application/pdf"},
    ]

    cols = st.columns(5)
    for i, fmt in enumerate(formats):
        with cols[i]:
            create_download_button(fig, fmt)
    
    json_str = json.dumps(latest_json_data, indent=2)
    with cols[0]:
        st.download_button(
            "**Save Data (JSON)**",
            json_str,
            file_name="pedigree_data.json",
            mime="application/json",
            use_container_width=True
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
    clear_matplotlib_cache()
    configure_fonts()
    st.set_page_config(
        page_title="HeredicTree",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()

    L = LANGUAGES[st.session_state[LANG_KEY]]
    
    st.title(L["title"])
    
    render_language_toggle(L)
        
    render_instructions(L)
    render_pedigree_generator(L)
    render_sidebar_data_loader(L)
    
    initialize_layout_defaults()
    live_config = render_layout_settings(L)
    
    edited_ind, edited_rel, current_meta = render_data_editor()
    
    latest_json_data = process_dataframe_for_json(
        edited_ind, edited_rel, current_meta, live_config
    )
    
    if latest_json_data:
        engine = PedigreeEngine(latest_json_data, live_config)
        positioned_nodes = engine.calculate_layout(
            adjustment_iterations=live_config['adjustment_iterations'],
            priority=live_config['layout_priority']
        )
        
        render_pedigree_output(
            positioned_nodes,
            latest_json_data["relationships"],
            live_config,
            latest_json_data
        )
    
    render_readme()


if __name__ == "__main__":
    main()
