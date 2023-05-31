#!/bin/bash

cd "$(dirname "$0")"
source ./.venv/bin/activate
source ./.env.local

if [ "$1" = "crawler" ]; then
    python3 ./src/crawl.py $2
elif [ "$1" = "compress" ]; then
    python3 ./src/compress.py
elif [ "$1" == "download" ]; then
    sftp -i $SFTP_IDENTITY_PATH -oPort=$SFTP_PORT $SFTP_USER@$SFTP_IP <<END
    lmkdir -p ./data
    lcd ./data
    cd "$SFTP_REMOTE_FOLDER/data"
    get -r *
    exit
END
fi


deactivate