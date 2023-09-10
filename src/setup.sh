#!/bin/bash

# check if python3 is installed
if ! [ -x "$(command -v python3)" ]; then
    echo '[!!] Error: python3 is not installed.' >&2
    exit 1
fi

# Check if pip is installed, upgrade if needed
python3 -m pip -V
if [ $? -eq 0 ]; then
    echo '[INSTALL] Found pip'
    if [[ $unamestr == 'Darwin' ]]; then
        python3 -m pip install --no-cache-dir --upgrade pip
    else
        python3 -m pip install --no-cache-dir --upgrade pip --user
    fi
else
    echo '[!!] Error: python3-pip not installed'
    exit 1
fi

echo 'Installing Requirements'
python3 -m pip install openpyxl
python3 -m pip install mysql.connector
python3 -m pip install pandas