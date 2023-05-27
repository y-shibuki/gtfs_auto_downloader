source ./.venv/bin/activate

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
fi

deactivate