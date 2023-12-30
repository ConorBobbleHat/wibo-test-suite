#!/bin/bash
# decomp.me is currently broken as a pep517 module, which means we can't just include it in our pyproject.toml
# (even as a local dependency via a submodule)
# As such: we need to do some schenanigans to get ourselves up and running (namely: hijacking decomp.me's poetry environment)

# Step 1: standard decomp.me backend install
git submodule update --init --recursive
poetry -C decomp.me/backend install --no-root
poetry -C decomp.me/backend run python decomp.me/backend/compilers/download.py

# Step 2: go round poetry, and inject extra dependencies we need using pip
# TODO: revisit this once decomp.me is pep517 compliant.
poetry -C decomp.me/backend run pip install multiprocess