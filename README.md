# HeredicTree

A web-based pedigree chart creation application following National Society of Genetic Counselors (NSGC) standards.

家系図作成アプリケーション（全米遺伝カウンセリング学会標準記載法準拠）

---

## Features / 機能

- **Interactive pedigree chart creation** / インタラクティブな家系図作成
- **NSGC-compliant notation** / NSGC準拠の記載法
- **JSON-based data management** / JSONベースのデータ管理
- **Multiple export formats** (SVG, PNG, PDF) / 複数の出力形式対応
- **Bilingual interface** (English/Japanese) / バイリンガルインターフェース
- **Sample datasets included** / サンプルデータセット付属

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
├── requirements.txt             # Python dependencies / Python依存関係
│
├── app/
│   ├── app.py                   # Main application / メインアプリケーション
│   ├── drawer.py                # Chart rendering / チャート描画
│   ├── engine.py                # Layout calculation / レイアウト計算
│   ├── utils.py                 # Utility functions / ユーティリティ関数
│   ├── parameter.py             # Parameter / パラメーター
│   ├── json_data.py             # Sample datasets / サンプルデータ
│   ├── pedigree_generator.py    # Easy Pedigree Generator / 簡易家系図作成
│   ├── translation.py           # Multiple language / 多言語対応
│   │
│   └── fonts/                   # Font files / フォントファイル
│       ├── NotoSans-Regular.ttf
│       ├── NotoSansJP-Regular.ttf
│       ├── NotoSansKR-Regular.ttf
│       ├── NotoSansSC-Regular.ttf
│       └── NotoSansTC-Regular.ttf
│   └── examples/                 # Example files / サンプルファイル
│       ├── 1. Simple_Pedigree.json
│       ├── 2. Habsburg_Pedigree.json
│       ├── 3. Angelina_Jolie.json
│       ├── 4. サザエさん.json
│       └── 5. Complex_Pedigree.json
```

---

## Usage / 使い方

1. **Load or upload data** / データの読み込みまたはアップロード
   - Use sample datasets or upload your own JSON file
   - サンプルデータを使用するか、独自のJSONファイルをアップロード

2. **Edit pedigree information** / 家系図情報の編集
   - Edit individuals and relationships in the table view
   - テーブルビューで個人情報と関係性を編集

3. **Adjust layout settings** / レイアウト設定の調整
   - Customize spacing, symbol size, and visual style
   - 間隔、シンボルサイズ、視覚スタイルをカスタマイズ

4. **Export your pedigree** / 家系図のエクスポート
   - Download as SVG, PNG, PDF, or JSON
   - SVG、PNG、PDF、またはJSON形式でダウンロード

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

- **meta**: Metadata and comments / メタデータとコメント
- **individual**: Person information / 個人情報
- **relationships**: Family relationships / 家族関係

See sample data files in `SampleData.py` for examples.

サンプルデータファイルは `SampleData.py` を参照してください。

---

## Version History / バージョン履歴

- **v20260107** - Initial public release / 初回公開リリース
- **v20260118** - Easy Pedigree Generator / 簡易家系図作成搭載

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

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

このHeredicTreeは、[クリエイティブ・コモンズ 表示 - 非営利 - 継承 4.0 国際 ライセンス][cc-by-nc-sa]の下に提供されています。

### License Summary / ライセンス概要

**You are free to / 以下の条件で自由に利用可能：**

- **Share** — Copy and redistribute the material / 共有 — 複製・再配布
- **Adapt** — Remix, transform, and build upon the material / 翻案 — 改変・二次創作

**Under the following terms / 以下の条件に従う必要があります：**

- **Attribution (BY)** — You must give appropriate credit / 表示 — 適切なクレジットを表示
- **NonCommercial (NC)** — You may not use the material for commercial purposes / 非営利 — 営利目的での利用禁止
- **ShareAlike (SA)** — Distribute derivative works under the same license / 継承 — 同一ライセンスで配布

### Credit / クレジット表示

```
Copyright (c) 2025 Tatsuro Yamaguchi
HeredicTree is licensed under CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/
```

### Important Notes / 重要事項

**Commercial Use Restrictions / 営利利用の制限：**

The following are considered commercial use and are **NOT permitted** without explicit permission:

以下は営利目的とみなされ、明示的な許可なしには**許可されません**：

- Publication, reproduction, or partial use in commercial contexts / 商業的な文脈での掲載・転載・一部利用
- Posting on corporate social media accounts / 企業アカウントでのSNS掲載
- Use in corporate seminars or presentations for customer acquisition / 企業主催の集客セミナー・講演での利用

**Exception / 例外：**
Internal use for employee training within a company is permitted.
企業内での社員教育目的での利用は可能です。

### Full License / 完全なライセンス条項

- [Commons Deed (Human-readable summary)][cc-by-nc-sa]
- [Legal Code (Full license)][cc-by-nc-sa-legal]

[cc-by-nc-sa]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-legal]: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

---

## Contact / お問い合わせ

For questions or licensing inquiries, please open an issue on GitHub.

質問やライセンスに関するお問い合わせは、GitHubのIssueを開いてください。

---

**HeredicTree** - Professional Pedigree Chart Creation Tool

Copyright (c) 2025 Tatsuro Yamaguchi
