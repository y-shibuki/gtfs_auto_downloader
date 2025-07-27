# GTFS Auto Downloader

## 概念図

![GTFS_Auto_Downloaderの概要](https://github.com/y-shibuki/gtfs_auto_downloader/assets/12867630/42d025eb-c010-48b9-922b-6c288b07de2c)

## 導入手順

### Linux 環境のセットアップ

#### 1. システム要件の確認

- Linux OS (Ubuntu 20.04+ 推奨)
- systemd (タイマー機能用)
- SSH/SFTP 接続設定 (データダウンロード用)

#### 2. 必要なパッケージのインストール

```bash
# 必要なシステムパッケージをインストール
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git rsync openssh-client build-essential

# プロジェクトのクローン
cd /home/$(whoami)/
git clone https://github.com/y-shibuki/gtfs_auto_downloader.git
cd gtfs_rt_crawler

# (未インストールの場合は）Homebrewのインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
source ~/.bashrc

# Taskのインストール
brew install go-task
task install
```

#### 4. 環境変数の設定

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
# SFTP設定（データダウンロード用）
SFTP_USER=your_username
SFTP_IP=your_server_ip
SFTP_PORT=22
SFTP_IDENTITY_PATH=/path/to/your/ssh/key
SFTP_REMOTE_FOLDER=/remote/path/to/data
FOLDER_PATH=/local/path/to/store/data

# API キー（各種GTFS RTフィード用）
# 使用するAPIに応じて設定
```

#### 5. 動作確認

```bash
# Taskを使った動作確認
task dev:test  # テスト実行（60秒間）

# 個別のクローラーをテスト実行
task crawler:20s   # 20秒間隔のクローラー
task crawler:60s   # 60秒間隔のクローラー
task crawler:120s  # 120秒間隔のクローラー

# 利用可能なタスク一覧を確認
task --list
```

## Taskfile を使ったコマンド実行

このプロジェクトでは、[Task](https://taskfile.dev/)を使ってコマンドを管理しています。

### 主要な Task コマンド

```bash
# 利用可能なタスク一覧を表示
task --list

# 開発環境のセットアップ
task dev:setup

# データクローラーの実行
task crawler:20s   # 20秒間隔
task crawler:60s   # 60秒間隔
task crawler:120s  # 120秒間隔
task crawler:1day  # 1日間隔

# データ操作
task compress      # データ圧縮
task decompress    # データ解凍
task download      # リモートサーバーからダウンロード

# systemd管理
task systemd:setup:crawler    # Crawlerサービス作成
task systemd:setup:downloader # Downloaderサービス作成
task systemd:enable:all       # 全タイマー有効化
task systemd:status           # タイマー状態確認
task systemd:stop:all         # 全タイマー停止

# その他
task clean         # クリーンアップ
task help          # 詳細ヘルプ
```

## 本番環境での自動実行設定

### Systemd Timers を使用した定期実行

#### 前提条件

- Linux 環境での導入手順が完了していること
- .env.local ファイルが正しく設定されていること
- プロジェクトディレクトリが /home/$(whoami)/gtfs_rt_crawler に配置されていること

#### セットアップ手順

1. サービスファイルの作成

Task を使ったサービス作成:

```bash
# Crawlerサービスの作成（データ収集用）
task systemd:setup:crawler

# Downloaderサービスの作成（データダウンロード用）
task systemd:setup:downloader
```

2. タイマーファイルの作成

タイマー設定例を確認:

```bash
./timer-examples.sh
```

実際にタイマーファイルを作成（例：20 秒間隔のクローラー）:

```bash
sudo tee /etc/systemd/system/gtfs-crawler-20s.timer > /dev/null <<EOF
[Unit]
Description=Run GTFS Crawler every 20 seconds
Requires=gtfs-crawler-20s.service

[Timer]
OnBootSec=30sec
OnUnitActiveSec=20sec
AccuracySec=1sec

[Install]
WantedBy=timers.target
EOF
```

3. systemd の設定確認とサービス有効化

Task を使った一括設定:

```bash
# 全てのタイマーを有効化
task systemd:enable:all
```

または個別に設定:

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

4. 動作確認とモニタリング

Task を使った確認:

```bash
# タイマー状態確認
task systemd:status

# サービスログ確認
task systemd:logs -- gtfs-crawler-20s.service

# 全タイマー停止
task systemd:stop:all
```

## サーバーに保管しているデータをローカルにダウンロードする手順

1. `.env.local`に、SFTP の通信に必要な情報を記入してください。
2. `bash main.sh download`でダウンロードができます。
3. `cron`で毎日ダウンロードするようにするのが良いでしょう。

## 構造

### フォルダ構造

```text
├── main.sh
└── src
    ├── Crawler
    │   ├── 120
    │   │   ├── KantoBus_TripUpdate.py
    │   │   └── KantoBus_VehiclePosition.py
    │   ├── 20
    │   │   ├── ToyamaChitetsuBus_TripUpdates.py
    │   │   ├── ToyamaChitetsuBus_VehiclePositions.py
    │   │   ├── ToyamaChitetsuTram_TripUpdates.py
    │   │   └── ToyamaChitetsuTram_VehiclePositions.py
    │   └── 60
    │       ├── Docomo_GBFS.py
    │       └── Hello_GBFS.py
    ├── compress.py
    ├── crawl.py
    └── decompress.py
```

### main.sh の使い方

```bash
main.sh crawler n
n: 実行間隔（秒数）
>> src/Crawler/nのフォルダ内にあるクローラーを実行する

main.sh compress
>> dataフォルダ内のデータを圧縮する

main.sh decompress
>> zipフォルダ内のデータを解凍する

main.sh download
>> サーバーからSFTP通信でデータをダウンロードする
```
