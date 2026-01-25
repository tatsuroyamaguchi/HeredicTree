import streamlit as st
import os

# 環境に応じて画像パスのプレフィックスを自動判定
# Docker環境: "./app/img/"
# GitHub Pages (stlite): "img/"
if os.path.exists("./app/img"):
    IMG_BASE = "./app/img/"
else:
    IMG_BASE = "img/"

def render_instructions(L):
    """Render instructions expander."""
    with st.expander("**How to Use**", expanded=False):
        st.markdown(L["how_to_use"])
        
        # Helper function to render sections cleanly
        def render_section(title, img_name, code_content):
            st.markdown(f"##### {title}")
            col1, col2 = st.columns([1, 2])
            with col1:
                # use_container_width=True でカラム幅に合わせて自動リサイズ（重なり防止）
                st.image(f"{IMG_BASE}{img_name}", use_container_width=True)
            with col2:
                st.markdown(code_content)

        # --- Sections ---

        render_section("Sex", "Sex.jpg", """
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children      |
            |I-1 |M     |        |I-1|I-2|II-1,II-2,II-3|
            |I-2 |F     |
            |II-1|M     |        Male
            |II-2|F     |        Female
            |II-3|N     |        Non-binary
            ```
            """)

        render_section("Gender", "Gender.jpg", """
            ```
            Individuals Table:  Relationships Table:
            |id  |gender|       |p1 |p2 |children      |
            |I-1 |M     |       |I-1|I-2|II-1,II-2,II-3|
            |I-2 |F     |
            |II-1|M     |       AFAB: Assigned Female At Birth
            |II-2|F     |       AMAB: Assigned Male At Birth
            |II-3|N     |       UAAB: Unassigned At Birth
            ```
            """)

        render_section("Proband/Client", "Proband.jpg", """
            ```
            Individuals Table:                 Relationships Table:
            |id   |gender|proband|client|       |p1  |p2  |children|
            |I-1  |M     |       |      |       |I-1 |I-2 |II-1    |
            |I-2  |F     |       |      |       |II-1|II-2|III-1   |
            |II-1 |M     |   x   |   x  |       Proband, Client
            |II-2 |F     |       |   x  |       Client
            |III-1|I     |       |      |
            ```
            """)

        render_section("Multiple Children", "Multiple_Children.jpg", """
            ```
            Individuals Table:  Relationships Table:
            |id  |gender|       |p1 |p2 |children      |
            |I-1 |M     |       |I-1|I-2|II-1,II-2,II-3|
            |I-2 |F     |
            |II-1|M3    |       Three males
            |II-2|F2    |       Two females
            |II-3|Nn    |       Unknown number of males and females
            ```
            """)

        render_section("Affected Status", "Affected_status.jpg", """
            ```
            Individuals Table:         Relationships Table:
            |id  |gender|affected |    |p1 |p2 |children           |
            |I-1 |M     |         |    |I-1|I-2|II-1,II-2,II-3,II-4|
            |I-2 |F     |         |
            |II-1|F     |A        |    A: affected
            |II-2|M     |A2-1     |    A2-1: affected in 1st disease of 2 diseases
            |II-3|F     |A4-2     |    A4-2: affected in 2nd disease of 4 diseases
            |II-4|M     |A4-1,A4-3|    A4-1,A4-3: affected in 1st and 3rd diseases of 4 diseases
            ```
            """)

        render_section("Pregnancy", "Pregnancy.jpg", """
            ```
            Individuals Table:         Relationships Table:
            |id  |gender|pregnancy|    |p1 |p2 |children|
            |I-1 |M     |         |    |I-1|I-2|II-1|
            |I-2 |F     |         |
            |II-1|N     |    x    |    Pregnancy
            ```
            """)

        render_section("Abortion", "Abortion.jpg", """
            ```
            Individuals Table:         Relationships Table:
            |id  |gender|deceased|     |p1 |p2 |children |
            |I-1 |M     |        |     |I-1|I-2|II-1,II-2|
            |I-2 |F     |        |
            |II-1|A     |        |     Spontaneous Abortion
            |II-2|A     |   x    |     Artificial Abortion
            ```
            """)

        render_section("Divorce", "Divorce.jpg", """
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children|divorced|
            |I-1 |M     |        |I-1|I-2|II-1    |D_p1    |
            |I-2 |F     |        D_p1: divorced line near p1 
            |II-1|F     |        D_p2: divorced line near p2
                                 D: divorced line in the middle
            ```
            """)

        render_section("Multiple Births", "Multiple.jpg", """
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children |multiples            |
            |I-1 |M     |        |I-1|I-2|II-1,II-2|II-1+II-2:monozygotic|
            |I-2 |F     |        monozygotic: identical twins
            |II-1|M     |        dizygotic: fraternal twins
            |II-2|M     |        unknown: unknown type
            ```
            """)

        render_section("Infertilty/No Children", "Infertilty.jpg", """
            ```
            Individuals Table:  Relationships Table:
            |id  |gender|       |p1 |p2 |children |
            |I-1 |M     |       |I-1|I-2|II-1,II-2|
            |I-2 |F     |
            |II-1|I     |       Infertilty
            |II-2|NC    |       No Children
            ```
            """)

        render_section("Donor", "Donor.jpg", """
            ```
            Individuals Table:      Relationships Table:
            |id  |gender|donor|     |p1 |p2 |children|
            |I-1 |M     |     |     |I-1|I-2|II-1    |
            |I-2 |F     |     |     |I-3|   |II-1    |
            |I-3 |F     |  x  |
            |II-1|F     |     |
            ```
            """)

        render_section("Surrogate", "Surrogate.jpg", """
            ```
            Individuals Table:          Relationships Table:
            |id  |gender|surrogate|     |p1 |p2 |children|
            |I-1 |M     |         |     |I-1|I-2|II-1    |
            |I-2 |F     |         |     |I-3|   |II-1    |
            |I-3 |F     |    x    |
            |II-1|F     |         |
            ```
            """)

        render_section("Adoption", "Adoption.jpg", """
            ```
            Individuals Table:  Relationships Table:
            |id  |gender|       |p1 |p2 |children|adopted_in |adopted_out|
            |I-1 |M     |       |I-1|I-2|II-1    |II-1       |II-2       |
            |I-2 |F     |
            |II-1|F     |       Adopted In
            |II-2|M     |       Adopted Out
            ```
            """)

        render_section("Consanguinity", "Consanguinity.jpg", """
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children|consanguinity|
            |I-1 |M     |        |I-1|I-2|II-1    |      x      |
            |I-2 |F     |
            |II-1|F     |
            ```
            """)

        render_section("Comments / Metadata", "Comments.jpg", """
            ```
            $\mathbf{BoldText}$
            $\mathit{ItalicText}$
            $X^{sup}$
            $X_{sub}$
            $\\alpha, \\beta, \gamma$
            '\\n' or 'Shift+Enter'
            $\mathbf{Germline}$: $\mathit{BRCA1}$: c.188T>A, p.L63X  
            $\mathbf{Created\ by}$: John Smith| Date: 2026-01-01  
            ```
            More LaTeX symbols: https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference
            """)
