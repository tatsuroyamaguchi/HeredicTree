# dictionary.py

LANGUAGES = {
    "English": {
        "title": "HeredicTree",
        "how_to_use": "1. Upload a JSON file via the sidebar or use the default data.  \n2. Edit individuals and relationships in the table view below.  \n3. Save data with **Download JSON**\n\n**JSON file format**:  \n\
            **Individuals**  \n\
            -- **gender**: M (Male), F (Female), N (Non-binary), A (Abortion), I (Infertility), NC (No Children), M3 (Male * 3), F2 (Female * 2), Nn (Non-binary * n)  \n\
            -- **affected**: A (Affected), A2-1 (right half), A2-2 (left half), A4-1 (top-right), A4-1,A4-3 (top-right and bottom-left), C (Carrier), D (Donor)  \n\
            -- **proband**: True/False or blank  \n\
            -- **client**: True/False or blank  \n\
            -- **documented**: True/False or blank  \n\
            -- **deceased**: True/False or blank  \n\
            -- **pregnancy**: True/False or blank  \n\
        **Relatives**  \n\
            -- **divorced**: D (Divorced at center), D_p1 (Divorced near p1), D_p2 (Divorced near p2)  \n\
            -- **children**: II-1,II-2 (if nessesary, separated by commas without space)  \n\
            -- **multiples**: II-3+II-4:monozygotic;II-5+II-6+II-7:dizygotic (format: ids separated by '+' , type after ':' , multiple sets separated by ';')  \n\
            -- **adopted_in**: III-1 (if nessesary, separated by commas without space)  \n\
            -- **adopted_out**: III-2 (if nessesary, separated by commas without space)  \n\
            -- **consanguinity**: True/False or blank  \n\
        **Metadata**  \n\
            -- **comments**: Any comments or notes regarding the pedigree data.  \n\
            -- Bold text: \$\mathbf{BoldText}\$  \n\
            -- Italic text: \$\mathit{ItalicText}\$  \n\
            -- Line break: Use two spaces at the end of a line  \n\
            -- Subscript: \$X_{sub}\$  \n\
            -- Superscript: \$X^{sup}\$  \n\
            -- Greek letters: \$\\alpha, \\beta, \\gamma\$ etc.  \n\
            -- More LaTeX symbols: https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference  \n\
        **National Society of Genetic Counselors (NSGC) Guidelines**:  \n\
            -- https://onlinelibrary.wiley.com/doi/10.1002/jgc4.1621",
        "paternal": "Paternal Siblings (M, F, M...)",
        "maternal": "Maternal Siblings (M, F, M...)",
        "self_generation": "Self (Proband) Generation (M, F, N...)",
        "father": "Father is which sibling number?",
        "mother": "Mother is which sibling number?",
        "self": "Self is which sibling number?",
        "sidebar_data_input": "Data Input",
        "upload_label": "Upload JSON file",
        "sample_files": "Sample Files",
        "load_example": "Load Example File",
        "load_ref": "Load Reference (Help)",
        "sidebar_layout_settings": "Layout Settings",
        "sub_spacing": "Spacing",
        "label_ps": "1. Partner spacing (minimum)",
        "help_ps": "Minimum horizontal spacing between partners.",
        "label_ms": "2. Sibling spacing (minimum)",
        "help_ms": "Minimum horizontal spacing between siblings.",
        "label_gh": "3. Generation spacing (vertical)",
        "help_gh": "Vertical spacing between generations.",
        "label_fg": "4. Family group spacing",
        "help_fg": "Horizontal spacing between different family groups.",
        "label_uso": "5. Connection line offset (depth)",
        "help_uso": "Depth offset for connection lines.",
        "label_ai": "6. Layout adjustment iterations",
        "help_ai": "Number of iterations for layout optimization. Higher values take more time but may improve layout.",
        "label_lp": "7. Layout Priority",
        "help_lp": "Choose the layout direction for the pedigree chart.",
        "lp_options": ["Children to Parents (Top-down)", "Parents to Children (Bottom-up)"],
        "sub_visual": "Visual Style",
        "label_ss": "8. Symbol size",
        "help_ss": "Size of the symbols (nodes) in the pedigree chart.",
        "label_lw": "9. Line width",
        "help_lw": "Width of the connection lines in the pedigree chart.",
        "label_fs": "10. Label font size",
        "help_fs": "Font size of the labels in the pedigree chart.",
        "label_lo": "11. Label vertical position",
        "help_lo": "Vertical position adjustment for labels in the pedigree chart.",
        "expander_edit": "Edit Data (Table View)",
        "sub_meta": "Metadata",
        "comments_label": "Comments",
        "sub_ind": "Individuals",
        "sub_rel": "Relationships",
        "chart_header": "Pedigree Chart",
        "download_header": "Download Options",
        "btn_json": "Download JSON",
        "success_load": "Loaded {} Data!"
    },
    "Japanese": {
        "title": "HeredicTree",
        "how_to_use": "1. サイドバーからJSONファイルをアップロードするか、デフォルトデータを使用します。  \n2. 下のテーブル表示で個人データと家族関係を編集します。  \n3. **Download JSON**でデータ保存\n\n**JSONファイル形式**:  \n\
            **個人データ (Individuals)**  \n\
            -- **gender**: M（男性）, F（女性）, N（ノンバイナリー）, A（中絶）, I（不妊）, NC（子供なし）, M3（男性×3）, F2（女性×2）, Nn（ノンバイナリー×n）  \n\
            -- **affected**: A（罹患）, A2-1（右半分）, A2-2（左半分）, A4-1（右上）, A4-1,A4-3（右上と左下）, C（保因者）, D（ドナー）  \n\
            -- **proband**: True/False または空欄  \n\
            -- **client**: True/False または空欄  \n\
            -- **documented**: True/False または空欄  \n\
            -- **deceased**: True/False または空欄  \n\
            -- **pregnancy**: True/False または空欄  \n\
        **家族関係 (Relationships)**  \n\
            -- **divorced**: D（中央に離婚マーク）, D_p1（p1側に離婚マーク）, D_p2（p2側に離婚マーク）  \n\
            -- **children**: II-1,II-2（必要に応じてカンマ区切りで複数指定、スペースなし）  \n\
            -- **multiples**: II-3+II-4:monozygotic;II-5+II-6+II-7:dizygotic（形式: '+'で区切ったID群、':'の後に多胎種別、';'で複数セット区切り）  \n\
            -- **adopted_in**: III-1（必要に応じてカンマ区切りで複数指定、スペースなし）  \n\
            -- **adopted_out**: III-2（必要に応じてカンマ区切りで複数指定、スペースなし）  \n\
            -- **consanguinity**: True/False または空欄  \n\
        **メタデータ**  \n\
            -- **comments**: 家系図データに関する備考・コメント  \n\
            -- 太字: \$\mathbf{BoldText}\$  \n\
            -- 斜体: \$\mathit{ItalicText}\$  \n\
            -- 改行: 行末にスペース2つ  \n\
            -- 下付き文字: \$X_{sub}\$  \n\
            -- 上付き文字: \$X^{sup}\$  \n\
            -- ギリシャ文字: \$\\alpha, \\beta, \\gamma\$  \n\
            -- その他LaTeX記法: https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference  \n\
        **米国遺伝カウンセリング学会 (NSGC) ガイドライン**:  \n\
            -- https://onlinelibrary.wiley.com/doi/10.1002/jgc4.1621",
        "paternal": "父方の兄弟姉妹 (M, F, M...)",
        "maternal": "母方の兄弟姉妹 (M, F, M...)",
        "self_generation": "本人(発端者)世代 (M, F, N...)",
        "father": "父は同胞の何番目？",
        "mother": "母は同胞の何番目？",
        "self": "本人は同胞の何番目？",
        "sidebar_data_input": "データ入力",
        "upload_label": "JSONファイルをアップロード",
        "sample_files": "サンプルファイル",
        "load_example": "読み込み",
        "load_ref": "リファレンス（ヘルプ）",
        "sidebar_layout_settings": "レイアウト設定",
        "sub_spacing": "間隔調整",
        "label_ps": "1. パートナー間の間隔 (最小)",
        "help_ps": "パートナー同士の最小水平間隔を設定します。",
        "label_ms": "2. 兄弟間の間隔 (最小)",
        "help_ms": "兄弟同士の最小水平間隔を設定します。",
        "label_gh": "3. 世代間の高さ (垂直方向)",
        "help_gh": "各世代間の垂直間隔を設定します。",
        "label_fg": "4. 家族グループ間の余白",
        "help_fg": "異なる家族グループ間の水平余白を設定します。",
        "label_uso": "5. 接続線のオフセット (深さ)",
        "help_uso": "接続線の深さ方向のオフセットを設定します。",
        "label_ai": "6. レイアウト調整の反復回数",
        "help_ai": "レイアウトの最適化を行う反復回数を設定します。値が大きいほど時間がかかりますが、配置が改善される場合があります。",
        "label_lp": "7. レイアウト優先順位",
        "help_lp": "家系図のレイアウト方向を選択します。",
        "lp_options": ["子から親へ", "親から子へ"],
        "sub_visual": "視覚スタイル",
        "label_ss": "8. シンボルのサイズ",
        "help_ss": "家系図上のシンボル（ノード）のサイズを設定します。",
        "label_lw": "9. 線の太さ",
        "help_lw": "家系図上の接続線の太さを設定します。",
        "label_fs": "10. ラベルのフォントサイズ",
        "help_fs": "家系図上のラベルのフォントサイズを設定します。",
        "label_lo": "11. ラベルの垂直位置",
        "help_lo": "家系図上のラベルの垂直位置を調整します。",
        "expander_edit": "データ編集（テーブル表示）",
        "sub_meta": "メタデータ",
        "comments_label": "備考・コメント",
        "sub_ind": "個人データ (Individuals)",
        "sub_rel": "家族関係 (Relationships)",
        "chart_header": "家系図プレビュー",
        "download_header": "ダウンロード・オプション",
        "btn_json": "JSONファイルをダウンロード",
        "success_load": "{}データを読み込みました！"
    }
}