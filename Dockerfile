# 使用するイメージを指定
# Astral uv を使用
FROM ghcr.io/astral-sh/uv:latest

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


# pyproject.tomlを、コンテナにコピー
COPY pyproject.toml /root/

# 作業ディレクトリを設定
WORKDIR /root

# uvを使ってパッケージをインストール
RUN uv sync --frozen

# DKRONの起動
CMD [ "dkron" , "agent", "--server", "--bootstrap-expect=1", "--data-dir=/dkron.data", "--node-name=node"]