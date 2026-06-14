# HeredicTree

A web-based pedigree chart creation application following National Society of Genetic Counselors (NSGC) standards.

家系図作成アプリケーション（全米遺伝カウンセリング学会標準記載法準拠）

---

## Use Online / ブラウザで今すぐ使う

You can use HeredicTree directly in your web browser without any installation.  
インストール不要で、以下のリンクからすぐに利用できます。

👉 **[https://tatsuroyamaguchi.github.io/HeredicTree/](https://tatsuroyamaguchi.github.io/HeredicTree/)**

---

## Features / 機能

- **Interactive pedigree chart creation** / インタラクティブな家系図作成
- **NSGC-compliant notation** / NSGC準拠の記載法
- **JSON-based data management** / JSONベースのデータ管理
- **Multiple export formats** (SVG, PNG, PDF) / 複数の出力形式対応
- **Bilingual interface** (English/Japanese/Español/Deutsch) / バイリンガルインターフェース
- **Easy Pedigree Generator** / 簡易家系図作成機能
- **Sample datasets included** / サンプルデータセット付属

---

## Format / フォーマット

| Individuals | Example | Relationships | Example |
|-------------|----------------|---------------|----------------|
| **id** | I-2 | **p1** | I-1 |
| **gender** | M, F, N | **p2** | I-2 |
| **affected** | A, A2-1 | **children** | II-1,II-2 |
| **label** | 46y. CRC | **note for relationships** | free comments |
| **note for individuals** | free comments | **divorced** | D_p1 |
| **proband** | check or blank | **multiples** | II-1+II-2:monozygotic |
| **client** | check or blank | **adopted_in** | II-1 |
| **carrier** | check or blank | **adopted_out** | II-2 |
| **documented** | check or blank | **consanguinity** | check or blank |
| **deceased** | check or blank |  |  |
| **pregnancy** | check or blank |  |  |
| **donor** | check or blank |  |  |
| **surrogate** | check or blank |  |  |

---

## Quick Start / クイックスタート

### Using Docker / Dockerを使用する場合

```bash
# Clone the repository / リポジトリをクローン
git clone https://github.com/tatsuroyamaguchi/HeredicTree.git
cd HeredicTree

# Build Docker image / Dockerイメージをビルド
docker build -t heredic_tree .

# Run container / コンテナを実行
docker run -d -p 8300:8300 --name HeredicTree heredic_tree
```

Access the application at: **http://localhost:8300**

アプリケーションにアクセス: **http://localhost:8300**

### Local Installation / ローカルインストール

```bash
# Install dependencies / 依存関係をインストール
pip install -r requirements.txt

# Run application / アプリケーションを起動
cd HeredicTree
streamlit run app.py --server.port 8080
```

Access the application at: **http://localhost:8080**

アプリケーションにアクセス: **http://localhost:8080**

---

## Requirements / 必要条件

- **Docker** (for containerized deployment / コンテナ化されたデプロイ用)
- **Python 3.11+** (for local execution / ローカル実行の場合)
- Modern web browser / モダンなウェブブラウザ

---

## Project Structure / ディレクトリ構成

```
HeredicTree/
├── README.md                    # This file / このファイル
├── Dockerfile                   # Docker configuration / Docker設定
├── index.html                   # Entry point for GitHub Pages / Web版エントリポイント
├── requirements.txt             # Python dependencies / Python依存関係
│
├── app/
│   ├── app.py                   # Main application / メインアプリケーション
│   ├── drawer.py                # Chart rendering / チャート描画
│   ├── engine.py                # Layout calculation / レイアウト計算
│   ├── instructions.py          # Instructions / インストラクション
│   ├── utils.py                 # Utility functions / ユーティリティ関数
│   ├── parameter.py             # Parameter / パラメーター
│   ├── pedigree_generator.py    # Easy Pedigree Generator / 簡易家系図作成機能
│   ├── translation.py           # Multiple language / 多言語対応
│   │
│   └── fonts/                   # Font files / フォントファイル
│       ├── NotoSans-Regular.ttf
│       ├── NotoSansJP-Regular.ttf
│       ├── NotoSansKR-Regular.ttf
│       ├── NotoSansSC-Regular.ttf
│       └── NotoSansTC-Regular.ttf
│   └── samples/                 # Sample files / サンプルファイル
│       ├── 1. Simple_Pedigree.json
│       ├── 2. Habsburg_Pedigree.json
│       ├── 3. Angelina_Jolie.json
│       ├── 4. サザエさん.json
│       └── 5. Complex_Pedigree.json
```

---

## Usage / 使い方

1. **Upload data** / データのアップロード
   - Upload a JSON file via the sidebar or use the Easy Pedigree Generator.
   - サイドバーからJSONファイルをアップロードするか、Easy Pedigree Generatorを使用します。

2. **Edit pedigree information** / 家系図情報の編集
   - Edit individuals and relationships in Edit Data (Table View).
   - Edit Data (Table View)で個人と家族関係を編集

3. **Adjust layout settings** / レイアウト設定の調整
   - Customize spacing, symbol size, and visual style
   - 間隔、シンボルサイズ、スタイルをカスタマイズ

4. **Export your pedigree** / 家系図のエクスポート
   - Download as SVG, PNG, JPG, TIFF, PDF, or JSON
   - SVG、PNG、JPG, TIFF, PDF、またはJSON形式でダウンロード

---

## Docker Management / Docker管理

### Rebuild container / コンテナの再構築

```bash
docker stop HeredicTree
docker rm HeredicTree
docker build -t heredic_tree .
docker run -d -p 8300:8300 --name HeredicTree heredic_tree
```

### View logs / ログを表示

```bash
docker logs HeredicTree
```

### Stop container / コンテナを停止

```bash
docker stop HeredicTree
```

---

## Data Format / データ形式

HeredicTree uses JSON format for pedigree data with three main sections:

HeredicTreeは家系図データにJSON形式を使用し、3つの主要セクションがあります：

- **individual**: Person information / 個人情報
- **relationships**: Family relationships / 家族関係
- **meta**: Metadata and comments / メタデータとコメント

---

## Version History / バージョン履歴

- **v20260126** - Implemented Notes feature. / Note機能を搭載
- **v20260125** - Made Proband and Client marker size adjustments independent. /　発端者とクライエントのサイズ調整を独立
- **v20260124** - Web version released (Stlite) / Web版公開
- **v20260118** - Easy Pedigree Generator / 簡易家系図作成機能搭載
- **v20260107** - Initial public release / 初回公開リリース
- **v1.0.0** - Zenodo release / zenodoリリース

---

## Contributing / 貢献

Bug reports and feature requests are welcome via GitHub Issues or Pull Requests.

バグ報告や機能追加の提案は、GitHubのIssuesまたはPull Requestsを通じてお願いします。

---

## Disclaimer / 免責事項

**English:**
The source code copyright belongs to Tatsuro Yamaguchi. This software is provided "as is" without warranty of any kind, express or implied, including but not limited to warranties of accuracy, completeness, effectiveness, reliability, safety, legality, or fitness for a particular purpose. No guarantee is made regarding the absence of security vulnerabilities, defects, errors, or bugs.

The author assumes no responsibility for any health issues, disadvantages, or troubles arising from the use of this program.

**日本語：**
本プログラムのソースコードの著作権は山口達郎に帰属しますが、正確性、完全性、有効性、信頼性、安全性、適法性、特定の目的への適合性を含む、事実上又は法律上の一切の不具合がないことにつき、明示的にも黙示的にも保証は行いません。なお、セキュリティ等への欠陥・エラー・バグがないことについても保証しません。

したがって、本プログラムの使用が原因で発生した健康被害や不利益、トラブルについては、山口達郎は一切の責任を負いません。

---

## License / ライセンス

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

本プロジェクトは、**GNU General Public License v3.0 (GPL-3.0)** の下でライセンスされています。

### License Summary / ライセンス概要

**Permissions / 許可されること:**
- ✅ **Commercial Use** / 商用利用
- ✅ **Modification** / 修正・改変
- ✅ **Distribution** / 再頒布
- ✅ **Private Use** / 私的利用

**Conditions / 条件:**
- ℹ️ **Disclose Source** / ソースコードの公開義務 (改変して配布する場合)
- ℹ️ **License and Copyright Notice** / ライセンスと著作権の表示
- ℹ️ **Same License** / 同一ライセンスでの配布 (コピーレフト)

**Limitations / 制限（無保証）:**
- ⚠️ **Liability** / 責任
- ⚠️ **Warranty** / 保証

For more details, please see the [LICENSE](LICENSE) file or visit [GNU.org](https://www.gnu.org/licenses/gpl-3.0.en.html).

詳細はリポジトリ内の [LICENSE](LICENSE) ファイル、または [GNU.org](https://www.gnu.org/licenses/gpl-3.0.ja.html) を参照してください。

### Credit / クレジット表示

```
Copyright (c) 2025 Tatsuro Yamaguchi 
HeredicTree is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
```

---
## Citation

引用の際は、以下の記載をお願いします。

If you use **HeredicTree** in your research, please cite it as follows:

### APA (7th edition)

> Yamaguchi, T., Kawai, K., Sasaki, K., Mori, Y., Yamada, T., Arai, M., Aruga, T., Hirata, K., & Ishida, H. (2026). *HeredicTree: A Python-based standardized pedigree drawing tool* (Version v1.0.0) [Computer software]. GitHub. https://github.com/tatsuroyamaguchi/HeredicTree

### Vancouver

> Yamaguchi T, Kawai K, Sasaki K, Mori Y, Yamada T, Arai M, Aruga T, Hirata K, Ishida H. HeredicTree: A Python-based standardized pedigree drawing tool [computer software]. Version 1.0.0. GitHub; 2026. Available from: https://github.com/tatsuroyamaguchi/HeredicTree

### BibTeX

```bibtex
@software{yamaguchi2026heredictree,
  author = {Yamaguchi, Tatsuro and Kawai, Koji and Sasaki, Kenta and Mori, Yoshinori and Yamada, Takashi and Arai, Masahiro and Aruga, Tetsuya and Hirata, Koji and Ishida, Hiroshi},
  title = {HeredicTree: A Python-based standardized pedigree drawing tool},
  version = {1.0.0},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/tatsuroyamaguchi/HeredicTree}
}
```

---

## Contact / お問い合わせ

For questions or licensing inquiries, please open an issue on GitHub.

質問やライセンスに関するお問い合わせは、GitHubのIssueを開いてください。

---

**HeredicTree** - Pedigree Generation Tool

Copyright (c) 2026 Tatsuro Yamaguchi
