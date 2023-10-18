#!/usr/bin/env bash

docker run --name gra_emb_fw --rm \
       --user "$(id -u):$(id -g)" \
       -v $PWD/data/input_data:/gra_emb_fw/data/input_data \
       -v $PWD/data/config:/gra_emb_fw/data/config \
       -v $PWD/data/embedding_result:/gra_emb_fw/data/embedding_result \
       -v $PWD/data/evaluation_result:/gra_emb_fw/data/evaluation_result \
       -v $PWD/data/output:/gra_emb_fw/data/output \
       gra_emb_fw &