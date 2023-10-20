# Usage

## Building and Saving the Docker Image
From the root directory of this repository, run the following command:

```terminal
docker/build.sh
```

This command will create a Docker image named `docker/gra_emb_fw.tar` and save it in the `docker/gra_emb_fw.zip` file, along with other scripts.

Subsequently, move the `docker/gra_emb_fw.zip` to the location where you intend to use it, and then execute the following commands:

```terminal
unzip gra_emb_fw.zip
cd gra_emb_fw/
./load.sh
```

These commands will unzip the `docker/gra_emb_fw.zip` file and load the Docker image.

## Running the Experiments
First, add the graphs as edgelists to `data/input_data/` directory and the configurations to `data/config` directory. Then, start the container by running:

```terminal
./run.sh
```

Once the container has started, you can use the following command to enter the container's bash:

```terminal
./enter.sh
```

If you want to use `screen` to be able to exit and later re-enter the container, this is the place to do it.

To leave the bash in the container, simply type:

```terminal
exit
```

Finally, to kill the container, use the following command:

```terminal
./kill.sh
```

## Result
After running the experiments, you could find the embedded graphs in the `gra_emb_fw/data/embedding_result/` directory, the evaluation results in the `gra_emb_fw/data/evaluation_result/` directory and the unified  `.csv` files in the `gra_emb_fw/data/output/` directory.