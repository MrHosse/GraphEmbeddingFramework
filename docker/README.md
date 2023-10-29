# Usage

## Building and Saving the Docker Image

In order to build a Docker image without zipping it, you can execute the following command in the root directory of this repository:

```terminal
docker/build.sh
```

This command will create a directory named `gra_emb_fw/` and save the Docker image along with the `run.sh` script inside it. You can later use this image as intented.

Alternatively, if you want to build the Docker image and then zip it, you can use the following command:

```terminal
docker/build.sh --zip
```

Executing this command will build the directory and compress it into a zip file. You can unzip this directory later in your desired destination.

In either case, you can navigate to `gra_emb_fw/` to run the experiments using the container.

## Running the Experiments

After copying your input graphs to `data/input_date/` and your configuarion settings to `data/config/`, simply use the following  command:

```terminal
./run.sh
```

This command, if necessary, loads the image and initiates the container. It also mounts the `data/` directory from the host file system to the container's file system, enabling you to modify input graphs in the `data/input_data/` directory and configure settings for embeddings and `main.py` in the `data/config/` directory. For more information on configuring embeddings, see [embedding/README.md](../embedding/README.md).

This command also computes the embedding and evaluation results automatically and terminates itself after finishing the calculations. After running the experiments, you will find the embedded graphs in the `data/embedding_result/` directory, the evaluation results in the `data/evaluation_result/` directory and the unified  `.csv` files in the `data/output/` directory.

In case you are only interested in computing the results for the example data that we provide, you can use:

```terminal
./run.sh --example
```

which works similarly to the previous command.

Alternatively, you could use the command:

```terminal
./run.sh --interactive
```

In addition to loading the image, initializing the container and mounting the necessary directories, this command lets you use the container's bash. Note that, unlike the last command, this command does NOT compute the results automatically, and you have to do that manually.

To enter the container's bash use:

```terminal
docker exec -it gra_emb_fw bash
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

To leave the bash in the container, simply type:

```terminal
exit
```

Finally, to terminate the container, use the following command:

```terminal
docker kill gra_emb_fw
```