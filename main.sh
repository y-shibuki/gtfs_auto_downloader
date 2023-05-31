#!/bin/bash

cd "$(dirname "$0")"
source ./.venv/bin/activate
source ./.env.local

if [ "$1" = "crawler" ]; then
    if [ $2 -eq 20 ]; then
        python3 20.py
    elif [ $2 -eq 60 ]; then
        python3 60.py
    elif [ $2 -eq 120 ]; then
        python3 120.py
    fi
elif [ "$1" = "compress" ]; then
    python3 compress.py
elif [ "$1" == "download" ]; then
    sftp -i $SFTP_IDENTITY_PATH -oPort=$SFTP_PORT $SFTP_USER@$SFTP_IP <<END
    lcd ./data
    cd "$SFTP_REMOTE_FOLDER/data"
    get *
    exit
END
fi


deactivate