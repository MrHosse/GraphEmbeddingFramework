#!/usr/bin/env bash

docker run --name gra_emb_fw --rm \
       --user "$(id -u):$(id -g)" \
       -v $PWD/input_data:/gra_emb_fw/input_data \
       -v $PWD/embedding_result:/gra_emb_fw/embedding_result \
       -v $PWD/evaluation_result:/gra_emb_fw/evaluation_result \
       -v $PWD/embedding/node2vec_exe:/gra_emb_fw/embedding/node2vec_exe \
       -v $PWD/embedding/struc2vec_exe/temp:/gra_emb_fw/embedding/struc2vec_exe/temp/ \
       -v $PWD/embedding/verse_exe/temp:/gra_emb_fw/embedding/verse_exe/temp/ \
       gra_emb_fw &