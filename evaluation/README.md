# Evaluations
This directory contains implementations for evaluation metrics.

## Link Prediction

Link Prediction is a concept in network analysis and graph theory, primarily applied in the context of social networks, biological networks and various other complex systems represented as graphs or networks. It involves predicting the likelihood or probability of the existence of a connection (or "link") between two nodes in a network based on the information available about the network's structure and the attributes of its nodes.

Here, we implement two different link prediction metrics, which evaluate an embedding method based on the result of the embedding and the input edgelist.

### Average Error Link Prediction
Given a specified optimal edge length, we could systematically assess all possible pairs of nodes to determine their connectivity status, and utilizte this to compute essential metrics, including recall, precision, and F-score. 

This evaluation metric iteratively evaluates these pairs across different edge lengths and identifies the edge length at which the F-score attains its maximum value, ultimately returning this optimized F-score value.

### Precision@k Link Prediction
Assuming that in an optimal embedding, a certain number of closest nodes to a specific node should be its actual neighbors, we can evaluate an embedding based on the likelihood that a node has its actual neighbors in its vicinity. This evaluation is referred to as precision@k.

This evaluation metric calculates the value for precision@k, where k is the arithmetic mean of node degrees. This value represents the arithmetic mean of the percentage of actual neighbors within the k nearest neighbors for every node.

## Read Time
This evaluation metric reads the time needed to calculate the embedding from the embedding result, where the required time is noted.

## Implementing Additional Evaluations
This framework is designed to be extensible, allowing for the addition of new evaluation metrics.

Keep in mind, that each evaluation metric should inherit from the [AbstractEvaluation](abstract_evaluation.py) and thus implement the method `evaluate_embedding()`, which reads an embedding from an embedding path and calculates the desired value. The resulting value will be printed alongside the primary `edgelist`, the `group` of the edgelist, the used `embedder`, the utilized `similarity_metric`, and the `type` of the computed value, formatted as follows:
```python
"edgelist,group,embedder,similarity_metric,type,value"
```
To generate an output line, use the `get_output_line(<type>, <value>)` function. You can print more than one line by concatenating the output lines together.

For more detailed information, please refer to the documentation in [AbstractEvaluation](abstract_evaluation.py).

# Similarity Metric
Each evaluation metric is initialized by a similarity metric to calculate how similar two nodes are.

## Euclidian Distance
This metric measures the distance between two nodes based on their positions in Euclidean geometry.

## Inner Product
This metric measures the distance between two nodes based on the inner product of their positional vectors.

## Implementing Additional Similarity Metrics
Each similarity metric should inherit from [AbstractSimilarityMetric](similarity_metric.py) and implement the `distance()` method, which calculates the distance between two nodes based on their positional vectors.
