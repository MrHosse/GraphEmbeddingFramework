#!/usr/bin/env bash

docker run --name gra_emb_fw --rm \
       --user "$(id -u):$(id -g)" \
       gra_emb_fw &