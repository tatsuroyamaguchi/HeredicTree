import streamlit as st

def render_instructions(L):
    """Render instructions expander."""
    with st.expander("**How to Use**", expanded=False):
        st.markdown(L["how_to_use"])
        st.markdown("##### Sex")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Sex.jpg", width=400)
        with col2:
            st.markdown("""
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
        st.markdown("##### Gender")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Gender.jpg", width=400)
        with col2:
            st.markdown("""
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
        st.markdown("##### Proband/Client")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Proband.jpg", width=400)
        with col2:
            st.markdown("""
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
        st.markdown("##### Multiple Children")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Multiple_Children.jpg", width=400)
        with col2:
            st.markdown("""
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
        st.markdown("##### Affected Status")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Affected_status.jpg", width=400)
        with col2:
            st.markdown("""
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
        st.markdown("##### Pregnancy")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Pregnancy.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:         Relationships Table:
            |id  |gender|pregnancy|    |p1 |p2 |children|
            |I-1 |M     |         |    |I-1|I-2|II-1|
            |I-2 |F     |         |
            |II-1|N     |    x    |    Pregnancy
            ```
            """)
        st.markdown("##### Abortion")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Abortion.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:         Relationships Table:
            |id  |gender|deceased|     |p1 |p2 |children |
            |I-1 |M     |        |     |I-1|I-2|II-1,II-2|
            |I-2 |F     |        |
            |II-1|A     |        |     Spontaneous Abortion
            |II-2|A     |   x    |     Artificial Abortion
            ```
            """)
        st.markdown("##### Divorce")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Divorce.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children|divorced|
            |I-1 |M     |        |I-1|I-2|II-1    |D_p1    |
            |I-2 |F     |        D_p1: divorced line near p1 
            |II-1|F     |        D_p2: divorced line near p2
                                 D: divorced line in the middle
            ```
            """)
        st.markdown("##### Multiple Births")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Multiple.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children |multiples            |
            |I-1 |M     |        |I-1|I-2|II-1,II-2|II-1+II-2:monozygotic|
            |I-2 |F     |        monozygotic: identical twins
            |II-1|M     |        dizygotic: fraternal twins
            |II-2|M     |        unknown: unknown type
            ```
            """)
        st.markdown("##### Infertilty/No Children")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Infertilty.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:  Relationships Table:
            |id  |gender|       |p1 |p2 |children |
            |I-1 |M     |       |I-1|I-2|II-1,II-2|
            |I-2 |F     |
            |II-1|I     |       Infertilty
            |II-2|NC    |       No Children
            ```
            """)
        st.markdown("##### Donor")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Donor.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:      Relationships Table:
            |id  |gender|donor|     |p1 |p2 |children|
            |I-1 |M     |     |     |I-1|I-2|II-1    |
            |I-2 |F     |     |     |I-3|   |II-1    |
            |I-3 |F     |  x  |
            |II-1|F     |     |
            ```
            """)
        st.markdown("##### Surrogate")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Surrogate.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:          Relationships Table:
            |id  |gender|surrogate|     |p1 |p2 |children|
            |I-1 |M     |         |     |I-1|I-2|II-1    |
            |I-2 |F     |         |     |I-3|   |II-1    |
            |I-3 |F     |    x    |
            |II-1|F     |         |
            ```
            """)
        st.markdown("##### Adoption")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Adoption.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:  Relationships Table:
            |id  |gender|       |p1 |p2 |children|adopted_in |adopted_out|
            |I-1 |M     |       |I-1|I-2|II-1    |II-1       |II-2       |
            |I-2 |F     |
            |II-1|F     |       Adopted In
            |II-2|M     |       Adopted Out
            ```
            """)
        st.markdown("##### Consanguinity")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Consanguinity.jpg", width=400)
        with col2:
            st.markdown("""
            ```
            Individuals Table:   Relationships Table:
            |id  |gender|        |p1 |p2 |children|consanguinity|
            |I-1 |M     |        |I-1|I-2|II-1    |      x      |
            |I-2 |F     |
            |II-1|F     |
            ```
            """)
        st.markdown("##### Comments / Metadata")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("./app/img/Comments.jpg", width=400)
        with col2:
            st.markdown("""
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