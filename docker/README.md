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

In order to run the experiments, you can specify the data directory using the `--data` argument with the `run.sh` command. Note that the path to the data directory can be both relative or absolute. Here's how to do it:

```terminal
./run.sh --data 'path/to/data/'
```

If you don't use the `--data` argument, the command will default to using the data directory in the root directory as the data path. Note that the specified data directory doesn't need to be named `data/`, but it should contain the input graphs in the `input_data/` subdirectory and configuration settings in the `config/` subdirectory.

This command will load the necessary image and initiate the container. It will mount the specified data directory from the host file system to the container's file system, allowing you to modify input graphs in the specified data directory and configure settings for embeddings and `main.py` within the `config/` subdirectory. For more information on configuring embeddings, refer to [embedding/README.md](../embedding/README.md).

The command will automatically perform the embedding and evaluation processes and terminate itself after completing the calculations. Once the experiments are done, you will find the embedded graphs in the `embedding_result/` subdirectory, the evaluation results in the `evaluation_result/` subdirectory and the unified  `.csv` files in the `output/` subdirectory.

In case you are only interested in computing the results for the example data that we provide, you can use:

```terminal
./run.sh --example
```

This command works similarly to the previous command, using `example/data/` directory as its data directory. After computing example graphs and configuration settings, it computes the experiment results.

Our examples include four different graph groups, each with 50 samples, and Zachary’s Karate Club graph as a standalone graph. For additional information, refer to [example/build_graph.py](example/build_graph.py).

In this context, we have also configured the use of two different variations of `node2vec`. For more details, see [example/build_config.py](example/build_config.py).

### Working with the Container

Alternatively, you could use the command:

```terminal
./run.sh --interactive
```

In addition to loading the image, initializing the container and mounting the data directory, this command lets you use the container's bash. Note that, unlike the last command, this command does NOT compute the results automatically, and you have to do that manually.

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