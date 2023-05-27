# GTFS Auto Downloader
## 使い方
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
make install
```
5. cronの設定
```
crontab -e
* * * * * for i in 0 20 40; do (sleep ${i}; $HOME/gtfs_auto_downloader/main.sh crawler 20) & done;
*/1 * * * * $HOME/gtfs_auto_downloader/main.sh crawler 60;
*/2 * * * * $HOME/gtfs_auto_downloader/main.sh crawler 120;
* 9 * * * $HOME/gtfs_auto_downloader/main.sh compress;
```
