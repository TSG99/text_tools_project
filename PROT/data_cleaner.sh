#!/bin/bash

bdir="Reddit_data/Raw"
outputdir="Reddit_data/Cleaned"

mkdir -p "$outputdir"

for state_dir in "${bdir}"/*/; do
    state_name=$(basename "$state_dir")

    output_file="${outputdir}/${state_name}_cleaned.txt"

    > "$output_file"

    for input_file in "${state_dir}"*.txt; do
        tail -n +2 "$input_file" | tr '[:upper:]' '[:lower:]' | sed "s/[^a-z0-9']/ /g" | sed '/^[[:space:]]*$/d' >> "$output_file"
    done
done

