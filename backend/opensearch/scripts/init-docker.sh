#!/bin/bash

# pass in the initial sleep time as an argument
if [ -z "$1" ]
then
  arg1="15"
else
  arg1="$1"
fi

# pass in the sleep interval as an argument
if [ -z "$2" ]
then
  arg2="5"
else
  arg2="$2"
fi

sleep $arg1
python3 ./opensearch/create_index.py ./opensearch/index.json $arg2
