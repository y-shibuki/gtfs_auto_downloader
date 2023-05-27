# GTFS Auto Downloader
## 使い方
1. pyenvを導入
```
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
make install
```
5. cronの設定
```
* * * * * for i in 0 20 40; do (sleep ${i}; $HOME/gtfs_auto_downloader/.venv/bin/python3 $HOME/gtfs_auto_downloader/20.py) & done;
*/1 * * * * $HOME/gtfs_auto_downloader/.venv/bin/python3 $HOME/gtfs_auto_downloader/60.py;
*/2 * * * * $HOME/gtfs_auto_downloader/.venv/bin/python3 $HOME/gtfs_auto_downloader/120.py;
* 9 * * * $HOME/gtfs_auto_downloader/.venv/bin/python3 $HOME/gtfs_auto_downloader/compress.py;
```
