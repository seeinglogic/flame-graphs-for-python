#!/bin/bash

set -ex

TAG="flame_graph_examples"
docker build -t $TAG .

# Run with a volume mount so files can be copied out
docker run --rm -it -v `pwd`:/host $TAG
