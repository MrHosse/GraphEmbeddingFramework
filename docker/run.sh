#!/usr/bin/env bash

docker run --name gra_emb_fw --rm \
       --user "$(id -u):$(id -g)" \
       -v $PWD/input_data:/gra_emb_fw/input_data \
       -v $PWD/embedding_result:/gra_emb_fw/embedding_result \
       -v $PWD/evaluation_result:/gra_emb_fw/evaluation_result \
       gra_emb_fw &