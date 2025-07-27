#!/bin/bash
cd "$(dirname "$0")"

if [ "$1" = "crawler" ]; then
    uv run python -m src.crawl $2
elif [ "$1" = "compress" ]; then
    uv run python -m src.compress
elif [ "$1" = "decompress" ]; then
    uv run python -m src.decompress
elif [ "$1" == "download" ]; then
    rsync -av -e "ssh -i $SFTP_IDENTITY_PATH -oPort=$SFTP_PORT" $SFTP_USER@$SFTP_IP:$SFTP_REMOTE_FOLDER/zip/ $FOLDER_PATH/zip
else
    echo "コマンドが不明です"
fi