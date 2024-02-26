#!/bin/bash

<<Block_comment 
Bash script must be in the same directory as the python script
Block_comment

# use absolute paths
grs_directory="/home/santiago/UCxn/grew_rules"
ud_directory="/home/santiago/data/treebanks/ud-treebanks-v2.13"

> errors.log

for grs_path in "$grs_directory"/*.grs; do
    if [ -e "$grs_path" ]; then
        grs=$(basename "$grs_path")
        if [[ "$grs" != *"German"* ]]; then
            treebank="${grs%.*}" #file name without extension
            echo "Processing treebank: $treebank"
            treebank_path="$ud_directory/$treebank"
            output_name="ucxn_${treebank,,}.conllu" #lowercase
            python3 ucxn_writing.py -i "$treebank_path" -o "$output_name" -cxn_grs "$grs"
        else
            echo "Ignoring $grs"
        fi
    fi
done