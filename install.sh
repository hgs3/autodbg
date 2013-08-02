#!/bin/bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


# Apples performTaskWithPathArgumentsTimeout requires you to give the full
# path to the script you'd like to run.  Its easier to reference the script
# if we install it to /usr/local/bin.

cp -f autodbg /usr/local/bin/
cp -f debugframe.py /usr/local/bin/
