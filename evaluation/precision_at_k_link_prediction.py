import math
import statistics
import sys
import os
import importlib
from abstract_evaluation import AbstractEvaluation

class PrecisionAtKLinkPrediction(AbstractEvaluation):
    
    def __init__(self, similarity_metric) -> None:
        super().__init__(similarity_metric)
    
    def evaluate_embedding(self, embedding_path, edgelist_path):
        # read the embedding
        embedding = dict()
        with open(embedding_path, 'r') as embf:
            lines = embf.read().split('\n')
            for line in lines:
                if line == '': continue
                coord = line.split(',')
                embedding[coord[0]] = list(map(float, coord[1:]))
        
        # hashing the node names from embedding using a list
        nodes = list(embedding.keys())
        
        # read edgelist
        edge_list = set()
        with open(edgelist_path, 'r') as edgef:
            edges = edgef.read().split('\n')
            for edge in edges:
                if edge == '': continue
                if not edge.split(' ')[0] == edge.split(' ')[1]:
                    node1 = nodes.index(edge.split(' ')[0])
                    node2 = nodes.index(edge.split(' ')[1])
                    edge_list.add(tuple(sorted([node1, node2])))
        
        # k is avg of node degrees
        k = round((2 * len(edge_list)) / (len(nodes))) 

        neighbour_count = [0 for _ in nodes]
        for edge in edge_list:
            neighbour_count[edge[0]] += 1
            neighbour_count[edge[1]] += 1

        # build a list with every node pair and sort them based on distance
        pairs = list()
        for i in range(len(nodes)):
            node_list = []
            for j in range(len(nodes)):
                if i != j: node_list.append(j)
            node_list = sorted(node_list, key=lambda x: similarity_metric.distance(embedding[nodes[i]], embedding[nodes[x]]))
            pairs.append(node_list)
        
        # for every node calculate the amount of near neighbours
        prAtK = []
        for i in range(len(pairs)):
            near_edge_cnt = 0
            num_observ = k if neighbour_count[i] > k else neighbour_count[i]
            k_nearest_nodes = pairs[i][:num_observ]
            for node in k_nearest_nodes:
                if tuple(sorted([node, i])) in edge_list: near_edge_cnt += 1
            prAtK.append(near_edge_cnt / len(k_nearest_nodes))
        
        # return result as mean of PrAtK
        return statistics.fmean(prAtK)
    
    
    

if __name__ == '__main__':

    edgelist_path = sys.argv[1]
    eval_cases = sys.argv[2:]
    embeddings = list(map(lambda value: value.split('#')[0], eval_cases))
    embedding_paths = list(map(lambda embedding: 'embedding_result/' + embedding + '/' + edgelist_path, embeddings))
    sim_metrics = list(map(lambda value: value.split('#')[1], eval_cases))
    
    output = "\"graph\",\"embedder\",\"similarity_metric\",\"pk_ratio\"\n"

    for i in range(len(embeddings)):
        embedding = embeddings[i]
        sim_metric_str = sim_metrics[i]
        embedding_path = embedding_paths[i]

        # get the similarity metric
        sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
        module = importlib.import_module('evaluation.similarity_metric')
        similarity_metric = getattr(module, sim_metric_str)

        model = PrecisionAtKLinkPrediction(similarity_metric)
        score = model.evaluate_embedding(embedding_path=embedding_path, 
                                            edgelist_path=edgelist_path)
        
        output += ("\"" + edgelist_path + '\",\"' + embedding + '\",\"' + sim_metric_str + '\",' + str(score) + '\n')
    
    print(output)