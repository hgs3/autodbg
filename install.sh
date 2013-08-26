#!/bin/bash

# Apples performTaskWithPathArgumentsTimeout requires you to give the full
# path to the script you'd like to run.  Its easier to reference the script
# if we install it to /usr/local/bin.

cp -f autodbg.py /usr/local/bin/
cp -f debugframe.py /usr/local/bin/

ln -s /usr/local/bin/autodbg.py /usr/local/bin/autodbg


