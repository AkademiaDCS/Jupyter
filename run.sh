#!/bin/bash

export JUPLOCK=/home/admin/.juplock

function run {
    export PYTHONWARNINGS="ignore"
    setfont lat2-16 -m 8859-2

    echo $PASS | su -c "setterm -blank 0 -powerdown 0"

    bash jup.sh &> /dev/null &
    python3 panel.py
}

if mkdir $JUPLOCK &> /dev/null
then
    run
fi
