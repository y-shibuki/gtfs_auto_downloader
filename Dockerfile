# 使用するイメージを指定
# Python 3.11.3
FROM python:3.11.3-slim-buster

# 環境設定
USER root
RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

# DKRONのインストール
RUN echo "deb [trusted=yes] https://repo.distrib.works/apt/ /" | tee /etc/apt/sources.list.d/docker.list
RUN apt-get update
RUN apt-get install dkron

# pipのアップグレード
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# requirements.txtを、コンテナにコピー
COPY requirements.txt /root/
# requirements.txtに記載されているパッケージをインストール
RUN pip install -r /root/requirements.txt

# DKRONの起動
CMD [ "dkron" , "agent", "--server", "--bootstrap-expect=1", "--data-dir=/dkron.data", "--node-name=node"]