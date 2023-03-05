#!/bin/bash

# pass in the sleep time as an argument
if [ -z "$1" ]
then
  arg1="20"
else
  arg1="$1"
fi

sleep $arg1
python3 ./plugin_management/manager.py
