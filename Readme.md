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
2. 、poetryを導入
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
git 
```
