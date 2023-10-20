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
To get started, initiate the container by executing the following command:

```terminal
./run.sh
```

This command also mounts the `data/` directory from the host file system to the container's file system, enabling you to modify input graphs in the `data/input_data/` directory and configure settings for embeddings and `main.py` in the `data/config/` directory. For more information on configuring embeddings, see [embedding/README.md](../embedding/README.md).
 
Once the container has started, you can use the following command to enter the container's bash:

```terminal
./enter.sh
```

If you want to use `screen` to be able to exit and later re-enter the container, this is the place to do it.

To calculate embeddings for input graphs, use:

```terminal
python ./main.py layout
```

To evaluate the embeddings, use:

```terminal
python ./main.py evaluate
```

Or execute both operations simultaneously with:

```
python ./main.py layout evaluate
```

After running the experiments, you will find the embedded graphs in the `data/embedding_result/` directory, the evaluation results in the `data/evaluation_result/` directory and the unified  `.csv` files in the `data/output/` directory.

To leave the bash in the container, simply type:

```terminal
exit
```

Finally, to kill the container, use the following command:

```terminal
./kill.sh
```