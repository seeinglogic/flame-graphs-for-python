#!/bin/bash

# NOTE: this only works on examples that have instrumentation built in
#   see basic-example/example.py to see how this is done

VOLUME_MOUNT=/host
prof_file="output.prof"
folded_file="output.folded"
svg_file="flamegraph_self_profile.svg"

set -ex

cd basic-example

echo "Running script that includes cProfile profiling..."
python example.py --self-profile

flameprof --format log $prof_file > $folded_file

cd ..

./FlameGraph/flamegraph.pl basic-example/$folded_file > $svg_file

if [ -f $svg_file ]; then
    echo "[+] Created flamegraph $svg_file"
    # Copy out the file if container has the volume mount
    if [ -d "$VOLUME_MOUNT" ]; then
        chmod 777 $svg_file
        cp $svg_file $VOLUME_MOUNT
    fi
fi

