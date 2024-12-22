#!/bin/bash

inputdir="Reddit_data/Processed_Data"
outputdir="Reddit_data/Prepped"

mkdir -p "$outputdir"

declare -A state_group

current_group=""
while IFS= read -r line; do
    if [[ "$line" == \** ]]; then
        current_group=$(echo "$line" | sed 's/\*//g' | xargs)
    else
        state_group["$line"]=$current_group
    fi
done < "states.txt"

for state_file in "${inputdir}"/*_processed.csv; do
    state_name=$(basename "$state_file" "_processed.csv")
    
    output_file="${outputdir}/${state_name}_prepped.csv"

    echo "comment,state_group,region" > "$output_file"

    state_name_lower=$(echo "$state_name" | tr '[:upper:]' '[:lower:]')
    region="${state_group[$state_name_lower]}"

    first_line=true
    while IFS=, read -r comment state_group_column; do
        if [ "$first_line" = true ]; then
            first_line=false
        fi

        echo "\"$comment\",\"$state_group_column\",\"$region\"" >> "$output_file"
    done < "$state_file"
done

