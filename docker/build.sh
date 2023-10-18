#!/usr/bin/env bash

docker image build -t gra_emb_fw docker \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) 
docker save -o docker/gra_emb_fw.tar gra_emb_fw

cd docker/
mkdir -p gra_emb_fw/data/input_data/
mkdir -p gra_emb_fw/data/config/
mkdir -p gra_emb_fw/data/embedding_result/
mkdir -p gra_emb_fw/data/evaluation_result/
mkdir -p gra_emb_fw/data/output/

cp gra_emb_fw.tar gra_emb_fw/
cp enter.sh gra_emb_fw/
cp load.sh gra_emb_fw/
cp kill.sh gra_emb_fw/
cp run.sh gra_emb_fw/

rm gra_emb_fw.zip
zip -r gra_emb_fw.zip gra_emb_fw/
rm -rf gra_emb_fw/