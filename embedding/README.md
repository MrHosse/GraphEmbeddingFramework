# Embeddings 
This directory contains the implementations of embeddings.

## Spring
This embedding employs the Fruchterman-Reingold force-directed algorithm to position nodes. We utilize the `spring_layout()` function provided by [networkx](https://networkx.org).

To configure experiment parameters, create a `spring.json` file in the `data/config/` directory using the following JSON format:

```json
{
    "pos": [],
    "k": [],
    "fixed": [],
    "iterations": [],
    "threshold": [],
    "weight": [],
    "scale": [],
    "center": [],
    "dim": [],
    "seed": []
}
```

Each list should contain valid values, or `"default"` to use the default values provided by the implementation. If a value is not specified or the list is empty, the default value will be automatically applied for that parameter.

For more information about implmentation and valid values, refer to the [spring_layout documentation](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html#spring-layout).

## Kamada Kawai 
This embedding positions the nodes of a given graph based on Kamada-Kawai path-length cost-function. Similar to `Spring`, here we also utilize the function `kamada_kawai_layout()` by [networkx](https://networkx.org).

For configuration, set up a `kamada_kawai.json` file in `data/config/` directory using the following JSON format:

```json
{
    "dist": [],
    "pos": [],
    "weight": [],
    "scale": [],
    "center": [],
    "dim": []
}
```

Each list should contain valid values or `"default"` to use the default values provided by the implementation. If a value is not specified or the list is empty, the default value will be automatically applied for that parameter.

For more information about implmentation and valid values, refer to the [kamada_kawai_layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html) documentation.

## Node2vec 
Node2vec is an algorithmic framework for learning continuous feature representations for nodes in a graph, which can be used for various downstream machine learning tasks. For more information, refer to [node2vec](https://arxiv.org/abs/1607.00653).

For implementation, we use the high performance implementation provided by [SNAP](https://github.com/snap-stanford/snap/tree/master/examples/node2vec). You can find more information about parameters there.

To set up the parameters for experiments, create a `node2vec.json` file in `data/config/` directory using the following JSON format:

```json
{
    "dim": [],
    "walk_len": [],
    "num_walks": [],
    "con_size": [],
    "max_iter": [],
    "ret_p": [],
    "inout_p": []
}
```

Similar to other embeddings, each list should consist of valid values or `"default"` for the default value. If a parameter is missing or the list is empty, the default value will be used.

## Struc2vec 
The Struc2vec algorithm learns continuous representations for nodes in any graph and captures structural equivalence between nodes. For more information on how the algorithm works, see [struc2vec](https://arxiv.org/abs/1704.03165)

Here, we use the implementation provided by the following [repository](https://github.com/sebkaz/struc2vec/tree/master#struc2vec)

To set up the parameters for experiments, create a `struc2vec.json` file in `data/config/` directory using the following JSON format:

```json
{
    "dim": [],
    "walk_len": [],
    "num_walks": [],
    "window_size": [],
    "until_layer": [],
    "iter": [],
    "workers": [],
    "opt1": [],
    "opt2": [],
    "opt3": []
}
```

Similar to other embeddings, each list should consist of valid values or `"default"` for the default value. If a parameter is missing or the list is empty, the default value will be used.

## Verse
This embedding is based on [VERSE: Versatile Graph Embeddings from Similarity Measures](https://arxiv.org/abs/1803.04742). For implementation, we utilize the implementation provided by the following [repository](https://github.com/xgfs/verse).

To set up the parameters for experiments, create a `verse.json` file in `data/config/` directory using the following JSON format:

```json
{
    "dim": [],
    "alpha": [],
    "threads": [],
    "nsamples": [],
    "steps": [],
    "global_lr": []
}
```

Similar to other embeddings, each list should consist of valid values or `"default"` for the default value. If a parameter is missing or the list is empty, the default value will be used.


## Implementing Additional Embeddings
This framework is designed to be extensible, allowing for the addition of new embeddings.

To add a new embedding, you can take inspiration from the provided embeddings that are already implemented. Keep in mind that each embedding should be capable of reading parameter values from a JSON file placed in `data/config/NEW_EMBEDDING_NAME.json`. Additionally, each embedding should inherit from the [AbstractEmbedder](abstract_embedder.py) class and implement the following methods:

1. `create_run()`: This method creates a run for experiments based on possible parameter values.

2. `calculate_layout()`: This method calculates the embedding for a given graph and returns it as a string. 

Finally, the result string should be printed along with the initial path to the edgelist and the time needed for calculation.

For more detailed information, please refer to the documentation in [AbstractEmbedder](abstract_embedder.py).

Please keep in mind that if your new embedding requires specific system requirements, you may need to modify the [docker/dockerfile](../docker/dockerfile) to ensure that your embedding can run within Docker.