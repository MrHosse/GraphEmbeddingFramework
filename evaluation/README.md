# Evaluations
This directory contains implementations for evaluation metrics.

## Link Prediction

Link Prediction is a concept in network analysis and graph theory, primarily applied in the context of social networks, biological networks and various other complex systems represented as graphs or networks. It involves predicting the likelihood or probability of the existence of a connection (or "link") between two nodes in a network based on the information available about the network's structure and the attributes of its nodes.

Here, we implement two different link prediction metrics, which evaluate an embedding method based on the result of the embedding and the input edgelist.

## Average Error Link Prediction
This link prediction method searches for the optimal edge length. This means that based on a given edge length if two vertices are closer than the optimal value, they are seen as connected, otherwise not. Based on this evaluation, we calculate a recall and precision value, from which harmonic mean, the F-score is calculated.
This evaluation metric calculates the optimal edge length for which the F-score is the highest. The F-score is the harmonic mean of precision and recall.

## Precision@k Link Prediction
This evaluation metric, based on an embedding and an edgelist, calculates the value for precision@k, where k is the arithmetic mean of node degrees. This value represents the arithmetic mean of the percentage of actual neighbors within the k nearest neighbors for every node.

## Read Time
This evaluation metric measures the time needed to calculate the embedding from the embedding path.

## Implementing Additional Evaluations
This framework is designed to be extensible, allowing for the addition of new evaluation metrics.

Keep in mind, that each evaluation metric should inherit from the [AbstractEvaluation](abstract_evaluation.py) and thus implement the method `evaluate_embedding()`, which reads an embedding from an embedding path and calculates the desired value. 

The results will be printed along with other information such as `edgelist`, `group`, and `embedder`.

For more detailed information, please refer to the documentation in [AbstractEvaluation](abstract_evaluation.py).

# Similarity Metric
Each evaluation metric is initialized by a similarity metric to calculate how similar two nodes are.

## Euclidian Distance
This metric measures the distance between two nodes based on their positions in Euclidean geometry.

## Inner Product
This metric measures the distance between two nodes based on the inner product of their positional vectors.

## Implementing Additional Evaluations
Each similarity metric should inherit from [AbstractSimilarityMetric](similarity_metric.py) and implement the `distance()` method, which calculates the distance between two nodes based on their positional vectors.
