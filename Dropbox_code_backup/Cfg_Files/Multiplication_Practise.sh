#!/bin/bash

## Practising using multiplication in bash

echo "Input number: " $1

# result=$(( 2*1 ))

# echo "multiplication output: " $result

echo -n "Hello "
awk "BEGIN {print 100*$1}"