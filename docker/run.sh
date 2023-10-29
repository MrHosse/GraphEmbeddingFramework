#!/usr/bin/env bash

if ! docker images --format '{{.Repository}}' | grep -q "gra_emb_fw"; then
    echo "Loading the image..."
    docker load -i gra_emb_fw.tar
fi

if [ "$(docker ps -q -f name=gra_emb_fw)" ]; then
    echo "Stopping the existing container..."
    docker kill gra_emb_fw
fi

if [[ "$1" == '--interactive' ]]; then
    echo "Starting container bash..."
    docker run --name gra_emb_fw --rm -d \
        --user "$(id -u):$(id -g)" \
        -v $PWD/data/input_data:/gra_emb_fw/data/input_data \
        -v $PWD/data/config:/gra_emb_fw/data/config \
        -v $PWD/data/embedding_result:/gra_emb_fw/data/embedding_result \
        -v $PWD/data/evaluation_result:/gra_emb_fw/data/evaluation_result \
        -v $PWD/data/output:/gra_emb_fw/data/output \
        --entrypoint "sleep" \
        gra_emb_fw infinity
elif [[ "$1" == '--example' ]]; then
    echo "Computing examples and results..."
    docker run --name gra_emb_fw --rm -it \
        --user "$(id -u):$(id -g)" \
        -v $PWD/data/input_data:/gra_emb_fw/data/input_data \
        -v $PWD/data/config:/gra_emb_fw/data/config \
        -v $PWD/data/embedding_result:/gra_emb_fw/data/embedding_result \
        -v $PWD/data/evaluation_result:/gra_emb_fw/data/evaluation_result \
        -v $PWD/data/output:/gra_emb_fw/data/output \
        gra_emb_fw sh -c "example/setup.sh && python ./main.py layout evaluate"
else
    echo "Running the experiments..."
    docker run --name gra_emb_fw --rm -it \
        --user "$(id -u):$(id -g)" \
        -v $PWD/data/input_data:/gra_emb_fw/data/input_data \
        -v $PWD/data/config:/gra_emb_fw/data/config \
        -v $PWD/data/embedding_result:/gra_emb_fw/data/embedding_result \
        -v $PWD/data/evaluation_result:/gra_emb_fw/data/evaluation_result \
        -v $PWD/data/output:/gra_emb_fw/data/output \
        gra_emb_fw python ./main.py layout evaluate
fi