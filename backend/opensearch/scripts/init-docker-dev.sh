#!/bin/bash

# pass in the sleep time as an argument
if [ -z "$1" ]
then
  arg1="15"
else
  arg1="$1"
fi

sleep $arg1
python3 ./opensearch/create_index.py ./opensearch/index.json
