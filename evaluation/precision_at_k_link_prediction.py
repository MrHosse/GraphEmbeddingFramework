import math
import statistics
import sys
import os
import importlib
from abstract_evaluation import AbstractEvaluation

class PrecisionAtKLinkPrediction(AbstractEvaluation):
    
    given_node = list()
    embedding = dict()
    nodes = list()
    neighbour_count = dict()
    
    def __init__(self, similarity_metric) -> None:
        super().__init__(similarity_metric)
    
    def distance_from_given_node(node):
        return similarity_metric.distance(PrecisionAtKLinkPrediction.embedding[PrecisionAtKLinkPrediction.nodes[PrecisionAtKLinkPrediction.given_node]], 
                         PrecisionAtKLinkPrediction.embedding[PrecisionAtKLinkPrediction.nodes[node]])
    
    def evaluate_embedding(self, k, embedding_path, edgelist_path):
        # read the embedding
        embedding = dict()
        with open(embedding_path, 'r') as embf:
            lines = embf.read().split('\n')
            for line in lines:
                if line == '': continue
                coord = line.split(',')
                embedding[coord[0]] = list(map(float, coord[1:]))
        PrecisionAtKLinkPrediction.embedding = embedding
        nodes = list(embedding.keys())
        PrecisionAtKLinkPrediction.nodes = nodes
        
        # read edgelist
        edge_list = list()
        neighbour_count = dict()
        for node in nodes:
            neighbour_count[node] = 0
        with open(edgelist_path, 'r') as edgef:
            edges = edgef.read().split('\n')
            for edge in edges:
                if edge == '': continue
                if not edge.split(' ')[0] == edge.split(' ')[1]:
                    edge_list.append(sorted(edge.split(' ')))
                    neighbour_count[edge.split(' ')[0]] += 1
                    neighbour_count[edge.split(' ')[1]] += 1
        PrecisionAtKLinkPrediction.neighbour_count = neighbour_count
        
        # build a list with every node pair and sort them based on distance
        pairs = list()
        for i in range(len(nodes)):
            node_list = []
            for j in range(len(nodes)):
                if i != j: node_list.append(j)
            PrecisionAtKLinkPrediction.given_node = i
            node_list = sorted(node_list, key=similarity_metric.distance)
            pairs.append(node_list)
        
        # for every node calculate the amount of near neighbours
        k_nearest_neighbours = []
        for i in range(len(pairs)):
            near_edge_cnt = 0
            k_nearest_nodes = pairs[i] if len(pairs[i]) < k else pairs[i][:k]
            for node in k_nearest_nodes:
                if sorted([nodes[i], nodes[node]]) in edge_list: near_edge_cnt += 1
                
            k_nearest_neighbours.append(near_edge_cnt)
            
        # return result as map of nodes to number of k nearest nodes which are also edges
        result = dict()
        for i in range(len(nodes)):
            result[nodes[i]] = k_nearest_neighbours[i]
            
        return(result)
    
    
    

if __name__ == '__main__':
    
    edgelist_path = sys.argv[2]
    embedding_path = sys.argv[3]
    embedding_name = sys.argv[3].split('/')[1]
    k = int(sys.argv[1])
    evaluation_path = 'evaluation_result/' + '/'.join(edgelist_path.split('/')[:-1]) + '/precision_at_k_' + str(k) + '_link_prediction.csv'
    
    if not os.path.exists(evaluation_path):
        os.makedirs('/'.join(evaluation_path.split('/')[:-1]), exist_ok=True)
        with open(evaluation_path, 'w') as file:
            file.write("\"graph\",\"embedder\",\"pk_ratio\"\n")
    
    # get the similarity metric
    with open('/'.join(sys.argv[2].split('/')[:2]) + '/README.md', 'r') as file:
        sim_metric_str = file.read()
        sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
        module = importlib.import_module('embedding.similarity_metric')
        similarity_metric = getattr(module, sim_metric_str)
    
    model = PrecisionAtKLinkPrediction(similarity_metric)
    result = model.evaluate_embedding(embedding_path=embedding_path,
                                      edgelist_path=edgelist_path,
                                      k=k)
    scores = list()
    for key in list(result.keys()):
        score = result[key] / min(PrecisionAtKLinkPrediction.neighbour_count[key] / 2, k)
        scores.append(score)
    
    score = statistics.fmean(scores)
    with open(evaluation_path, 'a') as file:
        file.write('\"' + edgelist_path + '\",\"' + embedding_name + '\",' + str(score) + '\n')
    