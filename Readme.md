# GTFS Auto Downloader

## 概念図

![GTFS_Auto_Downloaderの概要](https://github.com/y-shibuki/gtfs_auto_downloader/assets/12867630/42d025eb-c010-48b9-922b-6c288b07de2c)

## 導入手順

### 1. システム要件

- Linux OS (Ubuntu 20.04+ 推奨)
- systemd (タイマー機能用)
- SSH/SFTP 接続設定 (データダウンロード用)

### 2. 必要なパッケージのインストール

```bash
# 必要なシステムパッケージをインストール
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git rsync openssh-client build-essential

# プロジェクトのクローン
cd /home/$(whoami)/
git clone https://github.com/y-shibuki/gtfs_auto_downloader.git
cd gtfs_auto_downloader

# Homebrewのインストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
source ~/.bashrc

# Taskのインストール
brew install go-task
task install
```

### 3. 環境変数の設定

```bash
# 環境設定ファイルを作成
cp .env .env.local

# .env.localファイルを編集して以下の情報を設定
# - 各種APIのライセンスキー
# - SFTPサーバーの接続情報（データダウンロード用）
vim .env.local
```

`.env.local`に設定が必要な項目：

```bash
# API キー（各種GTFS RTフィード用）
PTD_HS_KEY=
ODPT_KEY=
```

### 4. 動作確認

```bash
# 利用可能なタスク一覧を確認
task --list

# テスト実行
task crawler:20s
```

## Task コマンド

### データクローラーの実行

```bash
task crawler:20s   # 20秒間隔
task crawler:60s   # 60秒間隔
task crawler:120s  # 120秒間隔
task crawler:1day  # 1日間隔
```

### データ操作

```bash
task compress      # データ圧縮
task decompress    # データ解凍
task download      # リモートサーバーからダウンロード
```

### systemd 管理

```bash
task systemd:setup:crawler    # Crawlerサービス作成
task systemd:setup:downloader # Downloaderサービス作成
task systemd:enable:all       # 全タイマー有効化
task systemd:status           # タイマー状態確認
task systemd:stop:all         # 全タイマー停止
```

## 本番環境での自動実行設定

### 1. サービスファイルの作成

```bash
# Crawlerサービスの作成（データ収集用）
task systemd:setup:crawler

# Downloaderサービスの作成（データダウンロード用）
task systemd:setup:downloader
```

### 2. タイマーの有効化

一括設定:

```bash
# 全てのタイマーを有効化
task systemd:enable:all
```

個別設定:

```bash
# systemdの設定をリロード
sudo systemctl daemon-reload

# タイマーを有効化して開始
sudo systemctl enable --now gtfs-crawler-20s.timer
sudo systemctl enable --now gtfs-crawler-60s.timer
sudo systemctl enable --now gtfs-crawler-120s.timer
sudo systemctl enable --now gtfs-crawler-1day.timer
sudo systemctl enable --now gtfs-compress.timer
sudo systemctl enable --now gtfs-downloader.timer
```

### 3. 動作確認

```bash
# タイマー状態確認
task systemd:status

# 全タイマー停止
task systemd:stop:all
```

## データダウンロード

リモートサーバーからデータをダウンロードする手順：

### 1. `.env.local`に SFTP 接続情報を設定

`.env.local`に設定が必要な項目：

```bash
# SFTP設定（データダウンロード用）
SFTP_USER=your_username
SFTP_IP=your_server_ip
SFTP_PORT=22
SFTP_IDENTITY_PATH=/path/to/your/ssh/key
SFTP_REMOTE_FOLDER=/remote/path/to/data
FOLDER_PATH=/local/path/to/store/data
```

### 2. `task download`でデータダウンロードを実行

## プロジェクト構造

```text
├── setup.sh              # systemdサービス設定スクリプト
├── Taskfile.yml          # タスク定義ファイル
├── pyproject.toml        # Python依存関係
└── app/
    ├── data/             # 収集データ保存先
    ├── src/
    │   ├── crawl.py      # メインクローラー
    │   ├── compress.py   # データ圧縮
    │   ├── decompress.py # データ展開
    │   └── Crawler/      # 各種クローラー実装
    │       ├── 20/       # 20秒間隔クローラー
    │       ├── 60/       # 60秒間隔クローラー
    │       ├── 120/      # 120秒間隔クローラー
    │       └── 1day/     # 1日間隔クローラー
    └── utils/
        └── logger.py     # ログ機能
```
