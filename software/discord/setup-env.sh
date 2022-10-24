#!/bin/bash

if [ ! -d "./venv" ]
then
    echo "Setting up virtual environment for first time"
    python3 -m venv ./venv
    source ./venv/bin/activate
    python3 -m pip install -r requirements.txt
fi

echo "Activate environment with source ./venv/bin/activate"
source ./venv/bin/activate
