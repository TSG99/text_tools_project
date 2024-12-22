#!/bin/bash

processed_data_dir="Reddit_Data/Processed_Data"
mkdir -p "$processed_data_dir"

for state_file in Reddit_Data/Cleaned/*.txt; do
    state_name=$(basename "$state_file" .txt)
    state_name="${state_name/_cleaned/}" 
    state_name_lower=$(echo "$state_name" | tr '[:upper:]' '[:lower:]')

    processed_file="${processed_data_dir}/${state_name_lower}_processed.csv"

    echo "comment,state_group" > "$processed_file"

    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            echo "\"$line\",$state_name_lower" >> "$processed_file"
        fi
    done < "$state_file"
done

