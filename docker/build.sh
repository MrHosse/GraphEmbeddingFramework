#!/usr/bin/env bash

docker image build -t gra_emb_fw docker \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) 
docker save -o docker/gra_emb_fw.tar gra_emb_fw

cd docker/
mkdir gra_emb_fw/
mkdir gra_emb_fw/input_data/
mkdir gra_emb_fw/embedding_result/
mkdir gra_emb_fw/evaluation_result/
mkdir gra_emb_fw/output/

cp gra_emb_fw.tar gra_emb_fw/
cp enter.sh gra_emb_fw/
cp load.sh gra_emb_fw/
cp kill.sh gra_emb_fw/
cp run.sh gra_emb_fw/

rm gra_emb_fw.zip
zip -r gra_emb_fw.zip gra_emb_fw/
rm -rf gra_emb_fw/