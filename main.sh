#!/bin/bash

cd "$(dirname "$0")"
source ./.venv/bin/activate
source ./.env.local

if [ "$1" = "crawler" ]; then
    python3 ./src/crawl.py $2
elif [ "$1" = "compress" ]; then
    python3 ./src/compress.py
elif [ "$1" = "decompress" ]; then
    python3 ./src/decompress.py
elif [ "$1" == "download" ]; then
    rsync -av -e "ssh -i $SFTP_IDENTITY_PATH -oPort=$SFTP_PORT" $SFTP_USER@$SFTP_IP:$SFTP_REMOTE_FOLDER/zip/ $FOLDER_PATH/zip
else
    echo "コマンドが不明です"
fi

deactivate
