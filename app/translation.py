import streamlit as st

LANGUAGES = {
    "English": {
        "title": "HeredicTree",
        "how_to_use": "1. Upload a JSON file via the sidebar or use the default data.  \n2. Edit individuals and relationships in the table view below.  \n3. Save data with **Download JSON**\n\n**JSON file format**:  \n\
            **Individuals**  \n\
            -- **gender**: M (Male), F (Female), N (Non-binary), A (Abortion), I (Infertility), NC (No Children), M3 (Male * 3), F2 (Female * 2), Nn (Non-binary * n)  \n\
            -- **affected**: A (Affected), A2-1 (right half), A2-2 (left half), A4-1 (top-right), A4-2 (bottom-right), A4-3 (bottom-left), A4-4 (top-left)  \n\
            -- **proband**: True/False or blank  \n\
            -- **client**: True/False or blank  \n\
            -- **carrier**: True/False or blank  \n\
            -- **documented**: True/False or blank  \n\
            -- **deceased**: True/False or blank  \n\
            -- **pregnancy**: True/False or blank  \n\
            -- **donor**: True/False or blank  \n\
            -- **surrogate**: True/False or blank  \n\
        **Relatives**  \n\
            -- **children**: II-1,II-2 (if nessesary, separated by commas without space)  \n\
            -- **divorced**: D (Divorced at center), D_p1 (Divorced near p1), D_p2 (Divorced near p2)  \n\
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
        "advanced": "Advanced Settings",
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
            -- **affected**: A（罹患）, A2-1（右半分）, A2-2（左半分）, A4-1（右上）, A4-2（右下）, A4-3（左下）, A4-4（左上）  \n\
            -- **proband**: True/False または空欄  \n\
            -- **client**: True/False または空欄  \n\
            -- **carrier**: True/False または空欄  \n\
            -- **documented**: True/False または空欄  \n\
            -- **deceased**: True/False または空欄  \n\
            -- **pregnancy**: True/False または空欄  \n\
            -- **donor**: True/False または空欄  \n\
            -- **surrogate**: True/False または空欄  \n\
        **家族関係 (Relationships)**  \n\
            -- **children**: II-1,II-2（必要に応じてカンマ区切りで複数指定、スペースなし）  \n\
            -- **divorced**: D（中央に離婚マーク）, D_p1（p1側に離婚マーク）, D_p2（p2側に離婚マーク）  \n\
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
        "advanced": "詳細設定",
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
    },
    "Español": {
        "title": "HeredicTree",
        "how_to_use": "1. Cargue un archivo JSON a través de la barra lateral o use los datos predeterminados.  \n2. Edite los individuos y las relaciones en la vista de tabla a continuación.  \n3. Guarde los datos con **Descargar JSON**\n\n**Formato de archivo JSON**:  \n\
            **Individuos**  \n\
            -- **gender**: M (Masculino), F (Femenino), N (No binario), A (Aborto), I (Infertilidad), NC (Sin hijos), M3 (Masculino * 3), F2 (Femenino * 2), Nn (No binario * n)  \n\
            -- **affected**: A (Afectado), A2-1 (mitad derecha), A2-2 (mitad izquierda), A4-1 (arriba derecha), A4-2 (abajo derecha), A4-3 (abajo izquierda), A4-4 (arriba izquierda)  \n\
            -- **proband**: True/False o en blanco  \n\
            -- **client**: True/False o en blanco  \n\
            -- **carrier**: True/False o en blanco  \n\
            -- **documented**: True/False o en blanco  \n\
            -- **deceased**: True/False o en blanco  \n\
            -- **pregnancy**: True/False o en blanco  \n\
            -- **donor**: True/False o en blanco  \n\
            -- **surrogate**: True/False o en blanco  \n\
        **Parientes**  \n\
            -- **children**: II-1,II-2 (si es necesario, separados por comas sin espacio)  \n\
            -- **divorced**: D (Divorciado en el centro), D_p1 (Divorciado cerca de p1), D_p2 (Divorciado cerca de p2)  \n\
            -- **multiples**: II-3+II-4:monozygotic;II-5+II-6+II-7:dizygotic (formato: IDs separadas por '+' , tipo después de ':' , múltiples conjuntos separados por ';')  \n\
            -- **adopted_in**: III-1 (si es necesario, separados por comas sin espacio)  \n\
            -- **adopted_out**: III-2 (si es necesario, separados por comas sin espacio)  \n\
            -- **consanguinity**: True/False o en blanco  \n\
        **Metadatos**  \n\
            -- **comments**: Cualquier comentario o nota sobre los datos del pedigree.  \n\
            -- Texto en negrita: \$\mathbf{BoldText}\$  \n\
            -- Texto en cursiva: \$\mathit{ItalicText}\$  \n\
            -- Salto de línea: Use dos espacios al final de una línea  \n\
            -- Subíndice: \$X_{sub}\$  \n\
            -- Superíndice: \$X^{sup}\$  \n\
            -- Letras griegas: \$\\alpha, \\beta, \\gamma\$ etc.  \n\
            -- Más símbolos LaTeX: https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference  \n\
        **Pautas de la Sociedad Nacional de Consejeros Genéticos (NSGC)**:  \n\
            -- https://onlinelibrary.wiley.com/doi/10.1002/jgc4.1621",
        "paternal": "Hermanos paternos (M, F, M...)",
        "maternal": "Hermanos maternos (M, F, M...)",
        "self_generation": "Generación propia (proband) (M, F, N...)",
        "father": "¿El padre es qué número de hermano?",
        "mother": "¿La madre es qué número de hermano?",
        "self": "¿Uno mismo es qué número de hermano?",
        "sidebar_data_input": "Entrada de datos",
        "upload_label": "Cargar archivo JSON",
        "sample_files": "Archivos de muestra",
        "load_example": "Cargar archivo de ejemplo",
        "load_ref": "Cargar referencia (Ayuda)",
        "sidebar_layout_settings": "Configuración de diseño",
        "sub_spacing": "Espaciado",
        "label_ps": "1. Espaciado entre parejas (mínimo)",
        "help_ps": "Espaciado horizontal mínimo entre parejas.",
        "label_ms": "2. Espaciado entre hermanos (mínimo)",
        "help_ms": "Espaciado horizontal mínimo entre hermanos.",
        "label_gh": "3. Espaciado entre generaciones (vertical)",
        "help_gh": "Espaciado vertical entre generaciones.",
        "label_fg": "4. Espaciado entre grupos familiares",
        "help_fg": "Espaciado horizontal entre diferentes grupos familiares.",
        "advanced": "Configuración avanzada",
        "label_uso": "5. Desplazamiento de la línea de conexión (profundidad)",
        "help_uso": "Desplazamiento de profundidad para las líneas de conexión.",
        "label_ai": "6. Iteraciones de ajuste de diseño",
        "help_ai": "Número de iteraciones para la optimización del diseño. Valores más altos toman más tiempo pero pueden mejorar el diseño.",
        "label_lp": "7. Prioridad de diseño",
        "help_lp": "Elija la dirección de diseño para el gráfico de pedigree.",
        "lp_options": ["De hijos a padres (de arriba hacia abajo)", "De padres a hijos (de abajo hacia arriba)"],
        "sub_visual": "Estilo visual",
        "label_ss": "8. Tamaño del símbolo",
        "help_ss": "Tamaño de los símbolos (nodos) en el gráfico de pedigree.",
        "label_lw": "9. Grosor de la línea",
        "help_lw": "Grosor de las líneas de conexión en el gráfico de pedigree.",
        "label_fs": "10. Tamaño de fuente de la etiqueta",
        "help_fs": "Tamaño de fuente de las etiquetas en el gráfico de pedigree.",
        "label_lo": "11. Posición vertical de la etiqueta",
        "help_lo": "Ajuste de la posición vertical de las etiquetas en el gráfico de pedigree.",
        "expander_edit": "Editar datos (vista de tabla)",
        "sub_meta": "Metadatos",
        "comments_label": "Comentarios",
        "sub_ind": "Individuos",
        "sub_rel": "Relaciones",
        "chart_header": "Gráfico de pedigree",
        "download_header": "Opciones de descarga",
        "btn_json": "Descargar JSON",
        "success_load": "¡Datos de {} cargados!"
    },
    "Deutsch": {
        "title": "HeredicTree",
        "how_to_use": "1. Laden Sie eine JSON-Datei über die Seitenleiste hoch oder verwenden Sie die Standarddaten.  \n2. Bearbeiten Sie Personen und Beziehungen in der untenstehenden Tabellenansicht.  \n3. Speichern Sie die Daten mit **JSON herunterladen**\n\n**JSON-Dateiformat**:  \n\
            **Personen**  \n\
            -- **gender**: M (Männlich), F (Weiblich), N (Nicht-binär), A (Abtreibung), I (Unfruchtbarkeit), NC (Keine Kinder), M3 (Männlich * 3), F2 (Weiblich * 2), Nn (Nicht-binär * n)  \n\
            -- **affected**: A (Betroffen), A2-1 (rechte Hälfte), A2-2 (linke Hälfte), A4-1 (oben rechts), A4-2 (unten rechts), A4-3 (unten links), A4-4 (oben links)  \n\
            -- **proband**: True/False oder leer  \n\
            -- **client**: True/False oder leer  \n\
            -- **carrier**: True/False oder leer  \n\
            -- **documented**: True/False oder leer  \n\
            -- **deceased**: True/False oder leer  \n\
            -- **pregnancy**: True/False oder leer  \n\
            -- **donor**: True/False oder leer  \n\
            -- **surrogate**: True/False oder leer  \n\
        **Verwandte**  \n\
            -- **children**: II-1,II-2 (falls erforderlich, durch Kommas ohne Leerzeichen getrennt)  \n\
            -- **divorced**: D (In der Mitte geschieden), D_p1 (In der Nähe von p1 geschieden), D_p2 (In der Nähe von p2 geschieden)  \n\
            -- **multiples**: II-3+II-4:monozygotic;II-5+II-6+II-7:dizygotic (Format: IDs durch '+' getrennt, Typ nach ':' , mehrere Sätze durch ';' getrennt)  \n\
            -- **adopted_in**: III-1 (falls erforderlich, durch Kommas ohne Leerzeichen getrennt)  \n\
            -- **adopted_out**: III-2 (falls erforderlich, durch Kommas ohne Leerzeichen getrennt)  \n\
            -- **consanguinity**: True/False oder leer  \n\
        **Metadaten**  \n\
            -- **comments**: Alle Kommentare oder Notizen zu den Pedigree-Daten.  \n\
            -- Fettdruck: \$\mathbf{BoldText}\$  \n\
            -- Kursivschrift: \$\mathit{ItalicText}\$  \n\
            -- Zeilenumbruch: Verwenden Sie am Ende einer Zeile zwei Leerzeichen  \n\
            -- Tiefgestellt: \$X_{sub}\$  \n\
            -- Hochgestellt: \$X^{sup}\$  \n\
            -- Griechische Buchstaben: \$\\alpha, \\beta, \\gamma\$ etc.  \n\
            -- Weitere LaTeX-Symbole: https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference  \n\
        **Richtlinien der National Society of Genetic Counselors (NSGC)**:  \n\
            -- https://onlinelibrary.wiley.com/doi/10.1002/jgc4.1621",
        "paternal": "Paternale Geschwister (M, F, M...)",
        "maternal": "Maternale Geschwister (M, F, M...)",
        "self_generation": "Eigene Generation (Proband) (M, F, N...)",
        "father": "Welches Geschwisterkind ist der Vater?",
        "mother": "Welches Geschwisterkind ist die Mutter?",
        "self": "Welches Geschwisterkind sind Sie selbst?",
        "sidebar_data_input": "Dateneingabe",
        "upload_label": "JSON-Datei hochladen",
        "sample_files": "Beispieldateien",
        "load_example": "Beispieldatei laden",
        "load_ref": "Referenz laden (Hilfe)",
        "sidebar_layout_settings": "Layout-Einstellungen",
        "sub_spacing": "Abstand",
        "label_ps": "1. Partnerabstand (Minimum)",
        "help_ps": "Minimale horizontale Entfernung zwischen Partnern.",
        "label_ms": "2. Geschwisterabstand (Minimum)",
        "help_ms": "Minimale horizontale Entfernung zwischen Geschwistern.",
        "label_gh": "3. Generationsabstand (vertikal)",
        "help_gh": "Vertikaler Abstand zwischen Generationen.",
        "label_fg": "4. Abstand zwischen Familiengruppen",
        "help_fg": "Horizontaler Abstand zwischen verschiedenen Familiengruppen.",
        "advanced": "Erweiterte Einstellungen",
        "label_uso": "5. Verbindungslinienversatz (Tiefe)",
        "help_uso": "Tiefenversatz für Verbindungslinien.",
        "label_ai": "6. Layout-Anpassungsiterationen",
        "help_ai": "Anzahl der Iterationen zur Layout-Optimierung. Höhere Werte dauern länger, können das Layout jedoch verbessern.",
        "label_lp": "7. Layout-Priorität",
        "help_lp": "Wählen Sie die Layout-Richtung für das Pedigree-Diagramm.",
        "lp_options": ["Von Kindern zu Eltern (Top-down)", "Von Eltern zu Kindern (Bottom-up)"],
        "sub_visual": "Visueller Stil",
        "label_ss": "8. Symbolgröße",
        "help_ss": "Größe der Symbole (Knoten) im Pedigree-Diagramm.",
        "label_lw": "9. Linienbreite",
        "help_lw": "Breite der Verbindungslinien im Pedigree-Diagramm.",
        "label_fs": "10. Schriftgröße der Beschriftung",
        "help_fs": "Schriftgröße der Beschriftungen im Pedigree-Diagramm.",
        "label_lo": "11. Vertikale Position der Beschriftung",
        "help_lo": "Vertikale Positionsanpassung für Beschriftungen im Pedigree-Diagramm.",
        "expander_edit": "Daten bearbeiten (Tabellenansicht)",
        "sub_meta": "Metadaten",
        "comments_label": "Kommentare",
        "sub_ind": "Personen",
        "sub_rel": "Beziehungen",
        "chart_header": "Pedigree-Diagramm",
        "download_header": "Download-Optionen",
        "btn_json": "JSON herunterladen",
        "success_load": "{} Daten geladen!"
    }
}