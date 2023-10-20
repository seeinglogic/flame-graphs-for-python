#!/bin/bash


./make_self_profiled_flamegraph.sh
./make_flameprof_flamegraphs.sh basic-example/example.py
./make_inferno_flamegraphs.sh basic-example/example.py

# Took about 4 minutes in testing
./make_flameprof_flamegraphs.sh aoc-2023-19/a.py
# Took about 2 minutes in testing
./make_flameprof_flamegraphs.sh aoc-2023-19/a-opt.py

./make_flameprof_flamegraphs.sh sqlite-example/test_insert.py
