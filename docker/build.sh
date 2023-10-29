#!/usr/bin/env bash

docker image build -t gra_emb_fw docker \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) 

rm -rf gra_emb_fw/
mkdir -p gra_emb_fw/
docker save -o gra_emb_fw/gra_emb_fw.tar gra_emb_fw

mkdir -p gra_emb_fw/data/input_data/
mkdir -p gra_emb_fw/data/config/
mkdir -p gra_emb_fw/data/embedding_result/
mkdir -p gra_emb_fw/data/evaluation_result/
mkdir -p gra_emb_fw/data/output/

cp docker/run.sh gra_emb_fw/

if [[ "$1" == '--zip' ]]; then
    rm gra_emb_fw.zip
    zip -r gra_emb_fw.zip gra_emb_fw/
fi