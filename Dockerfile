FROM ubuntu:22.04
# Tested on ubuntu@sha256:0bced47fffa3361afa981854fcabcd4577cd43cebbb808cea2b1f33a3dd7f508

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
RUN apt-get install -y \
    git wget curl vim build-essential python3 python3-pip python-is-python3


WORKDIR /src/flamegraph

# Install original flamegraph tools
RUN git clone --depth=1 https://github.com/brendangregg/FlameGraph

# Pip install necessary things
RUN pip install flameprof 2>/dev/null


COPY basic-example/ ./basic-example
COPY sqlite-example/ ./sqlite-example
COPY aoc-2023-19/ ./aoc-2023-19
COPY *.sh ./

ENTRYPOINT ./make_flameprof_flamegraphs.sh basic-example/example.py
# Takes longer, but shows all options
#ENTRYPOINT ./make_all.sh