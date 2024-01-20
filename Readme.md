# GTFS Auto Downloader

## 概念図

![GTFS_Auto_Downloaderの概要](https://github.com/y-shibuki/gtfs_auto_downloader/assets/12867630/42d025eb-c010-48b9-922b-6c288b07de2c)

## 導入手順

1. Dockerを導入  

2. Docker Composeを導入  

3. gtfs_auto_downloaderのclone  

```bash
cd /home/******/
git clone https://github.com/y-shibuki/gtfs_auto_downloader.git
```

## サーバーに定期的にデータを保存する手順

1. 環境変数の設定  

```bash
cd gtfs_rt_crawler
```

```.env.local```に各種APIのライセンスキーを登録

```bash
docker compose build  
docker compose up -d
```
ssh接続すると、ローカルPCのlocalhost:8080でサーバー上のDKRONにアクセスすることが可能  
サーバーをシャットダウンしない限り、Dockerは永続的に稼働するので収集が止まることはない、はず  

2. DKRONの設定  

## サーバーに保管しているデータをローカルにダウンロードする手順

1. ```.env.local```に、SFTPの通信に必要な情報を記入してください。  
2. ```bash main.sh download```でダウンロードができます。  
3. ```cron```で毎日ダウンロードするようにするのが良いでしょう。  

## 構造

### フォルダ構造

```
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

### main.shの使い方

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
