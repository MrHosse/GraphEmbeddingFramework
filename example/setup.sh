#!/usr/bin/env bash

python example/build_graph.py
python example/build_config.py

mkdir -p data/

cp -ru example/data .

rm -rf example/data