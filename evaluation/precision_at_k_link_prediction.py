import math
import statistics
import sys
import os
import importlib
from abstract_evaluation import AbstractEvaluation

class PrecisionAtKLinkPrediction(AbstractEvaluation):
    """
    Based on an embedding and an edgelist, this evaluation metric calculates the value
    for precision@k where k is the arithmetic mean of node degrees.
    This value is the arithmetic mean of percentage of actuall neighbours within the k 
    nearest neighbours for every node.
    """
    def __init__(self, similarity_metric) -> None:
        super().__init__(similarity_metric)
    
    def evaluate_embedding(self, embedding_path):
        # read the embedding
        embedding = dict()
        with open(embedding_path, 'r') as embf:
            lines = embf.read().split('\n')
            
            edgelist_path =  lines[0].split(' ')[0]
            
            for line in lines[1:]:
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
        k = math.ceil((2 * len(edge_list)) / (len(nodes))) 
        
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

    embedding_path = sys.argv[1]
    with open(embedding_path, 'r') as embedding:
        edgelist = embedding.readline().split(' ')[0]
        group = edgelist.split('/')[2]
    sim_metric_str = sys.argv[2]
    embedding = embedding_path.split('/')[2]

    # get the similarity metric
    sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
    module = importlib.import_module('evaluation.similarity_metric')
    similarity_metric = getattr(module, sim_metric_str)
    
    model = PrecisionAtKLinkPrediction(similarity_metric)
    score = model.evaluate_embedding(embedding_path=embedding_path)
        
    output = f'{edgelist},{group},{embedding},{sim_metric_str},pk_ratio,{score}'
    
    print(output)