#!/bin/bash

set -ex


if [ ! -f $HOME/.cargo/env ]; then
    echo "Cargo not installed, installing it..."

    curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain nightly -y
else
    echo "Cargo already installed"
fi

source $HOME/.cargo/env

if ! command -v inferno-flamegraph &> /dev/null; then
    cargo install inferno
else
    echo "inferno already installed"
fi
