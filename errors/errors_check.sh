#!/bin/bash
# Launch from within 'errors' directory

FILE=$1
ARGS=$2
ERROR_FILES=*.csv
green="\033[32m"
bold="\033[1m"
reset="\033[0m"

print() {
    echo -e "$green$1$reset"
}

print "$bold\tARGUMENTS CHECK"
$FILE
$FILE hjfdg 435
$FILE test.csv

print "$bold\tERROR TESTS"
for f in $ERROR_FILES; do
    print $f
    $FILE $f $ARGS
done
print "$bold\tDOWNLOADED DATASET TESTS"
print "dataset_train.csv"
$FILE ../datasets/dataset_train.csv $ARGS
print "dataset_test.csv"
$FILE ../datasets/dataset_test.csv $ARGS