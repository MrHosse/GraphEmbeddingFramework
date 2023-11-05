#!/usr/bin/env bash

if ! docker images --format '{{.Repository}}' | grep -q "gra_emb_fw"; then
    echo "Loading the image..."
    docker load -i gra_emb_fw.tar
fi

if [ "$(docker ps -q -f name=gra_emb_fw)" ]; then
    echo "Stopping the existing container..."
    docker kill gra_emb_fw
fi

data_path="$PWD/data/"
run_type="default"

while [[ $# -gt 0 ]]; do 
    case "$1" in 
        --data)
            shift 
            data_path="$1"
            shift
            ;;
    	--interactive)
            run_type="interactive"
            shift
            ;;
        --example)
            run_type="example"
            shift
            ;;
    *)
        shift
        ;;
    esac
done

if [[ $data_path != /* ]]; then
    data_path="$PWD/$data_path"
fi

if [[ $run_type == "interactive" ]]; then
    echo "Starting container bash..."
    mkdir -p "$data_path"input_data
    mkdir -p "$data_path"config
    mkdir -p "$data_path"embedding_result
    mkdir -p "$data_path"evaluation_result
    mkdir -p "$data_path"output
    docker run --name gra_emb_fw --rm -d \
        --user "$(id -u):$(id -g)" \
        -v "$data_path"input_data:/gra_emb_fw/data/input_data \
        -v "$data_path"config:/gra_emb_fw/data/config \
        -v "$data_path"embedding_result:/gra_emb_fw/data/embedding_result \
        -v "$data_path"evaluation_result:/gra_emb_fw/data/evaluation_result \
        -v "$data_path"output:/gra_emb_fw/data/output \
        --entrypoint "sleep" \
        gra_emb_fw infinity
elif [[ $run_type == "example" ]]; then
    echo "Computing examples and results..."
    mkdir -p $PWD/example/data/input_data
    mkdir -p $PWD/example/data/config
    mkdir -p $PWD/example/data/embedding_result
    mkdir -p $PWD/example/data/evaluation_result
    mkdir -p $PWD/example/data/output
    docker run --name gra_emb_fw --rm -it \
        --user "$(id -u):$(id -g)" \
        -v $PWD/example/data/input_data:/gra_emb_fw/data/input_data \
        -v $PWD/example/data/config:/gra_emb_fw/data/config \
        -v $PWD/example/data/embedding_result:/gra_emb_fw/data/embedding_result \
        -v $PWD/example/data/evaluation_result:/gra_emb_fw/data/evaluation_result \
        -v $PWD/example/data/output:/gra_emb_fw/data/output \
        gra_emb_fw sh -c "example/setup.sh && python ./main.py layout evaluate"
else
    echo "Running the experiments..."
    mkdir -p "$data_path"input_data
    mkdir -p "$data_path"config
    mkdir -p "$data_path"embedding_result
    mkdir -p "$data_path"evaluation_result
    mkdir -p "$data_path"output
    docker run --name gra_emb_fw --rm -it \
        --user "$(id -u):$(id -g)" \
        -v "$data_path"input_data:/gra_emb_fw/data/input_data \
        -v "$data_path"config:/gra_emb_fw/data/config \
        -v "$data_path"embedding_result:/gra_emb_fw/data/embedding_result \
        -v "$data_path"evaluation_result:/gra_emb_fw/data/evaluation_result \
        -v "$data_path"output:/gra_emb_fw/data/output \
        gra_emb_fw python ./main.py layout evaluate
fi