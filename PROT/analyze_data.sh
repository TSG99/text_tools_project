#!/bin/bash

inputdir="Reddit_data/Cleaned"
outputdir="Reddit_data/Analyze"

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

for state_file in "${inputdir}"/*_cleaned.txt; do
    state_name=$(basename "$state_file" "_cleaned.txt")

    state_name_lower=$(echo "$state_name" | tr '[:upper:]' '[:lower:]')
    region="${state_group[$state_name_lower]}"

    output_file="${outputdir}/${region}.txt"

    grep -oE '\b\w+\b' "$state_file" >> "$output_file"

    echo "Extracted words from $state_name into $output_file."
done

