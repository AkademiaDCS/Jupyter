#!/bin/bash

export JUPLOCK=/home/admin/.juplock

function run {
    bash jup.sh &> /dev/null &
    python3 panel.py
}

if mkdir $JUPLOCK &> /dev/null
then
    run
fi
