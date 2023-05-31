# GTFS Auto Downloader
## 概念図
![GTFS_Auto_Downloaderの概要](https://github.com/y-shibuki/gtfs_auto_downloader/assets/12867630/42d025eb-c010-48b9-922b-6c288b07de2c)
## 導入手順
1. pyenvを導入  
```
sudo apt install build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo '' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
source ~/.bashrc

pyenv -v
# ここでバージョンが表示されたら成功
pyenv install 3.11.3
```
2. poetryを導入  
```
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/home/******/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
poetry --version
# ここでバージョンが表示されたら成功
poetry config virtualenvs.in-project true
```
3. gtfs_auto_downloaderのclone  
```
cd /home/******/
git clone https://github.com/y-shibuki/gtfs_auto_downloader.git
```
4. 環境設定  
```
pyenv local 3.11.3
poetry env use 3.11.3
poetry install
```
## サーバーに定期的にデータを保存する手順
1. 環境変数の設定  
```.env.local```に各種APIのライセンスキーを入力
2. cronの設定  
```
crontab -e
* * * * * for i in 0 20 40; do (sleep ${i}; bash $HOME/gtfs_auto_downloader/main.sh crawler 20) & done;
*/1 * * * * bash $HOME/gtfs_auto_downloader/main.sh crawler 60;
*/2 * * * * bash $HOME/gtfs_auto_downloader/main.sh crawler 120;
* 9 * * * bash $HOME/gtfs_auto_downloader/main.sh compress;
```
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
```
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