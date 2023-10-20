#!/bin/bash

VOLUME_MOUNT=/host

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_python_file>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "File \"$1\" does not exist."
    exit 1
fi

# Extract names/paths
file_path="$1"
file_dir=$(dirname "$file_path")
file_name=$(basename -- "$file_path")
name="${file_name%.*}"

# Set up output filenames
out_prefix="$file_dir/$name"
prof_file="${out_prefix}.prof"
folded_file="${out_prefix}.folded"
svg_file="${file_dir}/flamegraph_${name}.svg"

set -ex

python -m cProfile -o $prof_file $file_path

flameprof --format log $prof_file > $folded_file

./FlameGraph/flamegraph.pl $folded_file > $svg_file

if [ -f $svg_file ]; then
    echo "[+] Created flamegraph $svg_file"
    # Copy out the file if container has the volume mount
    if [ -d "$VOLUME_MOUNT" ]; then
        chmod 777 $svg_file
        cp $svg_file $VOLUME_MOUNT
    fi
fi
