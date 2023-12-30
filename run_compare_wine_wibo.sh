#!/bin/bash
poetry -C decomp.me/backend run python compile_tests.py "$1" wibo
poetry -C decomp.me/backend run python compare_compilations.py wine wibo