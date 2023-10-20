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

set -e

# Install rust/inferno if we don't have it
if [ ! -f $HOME/.cargo/env ]; then

    ./install_inferno.sh

    source $HOME/.cargo/env

    if ! command -v inferno-flamegraph &> /dev/null; then
        echo "Failed to install inferno..."
        exit 1
    fi
else
    source $HOME/.cargo/env
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
svg_file="$file_dir/flamegraph_inferno_${name}.svg"
svg_reverse_file="$file_dir/flamegraph_inferno_reverse_${name}.svg"

set -x

python -m cProfile -o $prof_file $file_path

flameprof --format log $prof_file > $folded_file

#inferno-flamegraph $folded_file > $svg_file
inferno-flamegraph --height 30 --stroke-color '#0f0f0f' $folded_file > $svg_file
inferno-flamegraph --height 30 --stroke-color '#0f0f0f' --reverse $folded_file > $svg_reverse_file
# Other options to look into: --consistent, --colordiffusion, --inverted

if [ -f $svg_file ] && [ -f $svg_reverse_file ]; then
    echo "[+] Created flamegraphs $svg_file and $svg_reverse_file"
    # Copy out the file if container has the volume mount
    if [ -d "$VOLUME_MOUNT" ]; then
        chmod 777 $svg_file $svg_reverse_file
        cp $svg_file $svg_reverse_file $VOLUME_MOUNT
    fi
fi
