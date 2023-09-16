import sys
import os
from abstract_evaluation import AbstractEvaluation
import importlib

class AverageErrorLinkPrediction(AbstractEvaluation):
    
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

        # read edgelist and ignore loops
        edge_list = set()
        with open(edgelist_path, 'r') as edgef:
            edges = edgef.read().split('\n')
            for edge in edges:
                if edge == '': continue
                if not edge.split(' ')[0] == edge.split(' ')[1]:
                    node1 = nodes.index(edge.split(' ')[0])
                    node2 = nodes.index(edge.split(' ')[1])
                    edge_list.add(tuple(sorted([node1, node2])))
        
        # save all node pairs to find the optimal edge length
        node_pairs = list()
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if (tuple([i, j]) in edge_list):
                    node_pairs.append(ListEntity(nodes=[nodes[i], nodes[j]], 
                                    distance=similarity_metric.distance(embedding[nodes[i]], embedding[nodes[j]]), 
                                    isEdge=True))
                else:
                    node_pairs.append(ListEntity(nodes=[nodes[i], nodes[j]], 
                                    distance=similarity_metric.distance(embedding[nodes[i]], embedding[nodes[j]]), 
                                    isEdge=False))
        
        # sort based on distance
        sorted_node_pairs = sorted(node_pairs, key=lambda x: x.distance)
        
        # find the optimal length
        left_edges = 0
        m = len(edge_list)
        
        optimal_precision = -1
        optimal_recall = -1
        optimal_f_score = -1
        
        for i in range(len(sorted_node_pairs)):
            pair = sorted_node_pairs[i]
            if (pair.isEdge): left_edges += 1
            
            # calculate the harmonic mean of edge ration on left side and non edge ratio on right side
            current_precision = left_edges / (i + 1)
            current_recall = left_edges / m
            current_f_score = 0 if (current_precision + current_recall == 0) else (2 * current_precision * current_recall) / (current_recall + current_precision)

            if (current_f_score > optimal_f_score):
                optimal_f_score = current_f_score
                optimal_precision = current_precision
                optimal_recall = current_recall
        
        return [optimal_precision, optimal_recall, optimal_f_score] 
        
class ListEntity:
    
    def __init__(self, nodes, distance, isEdge):
        self.nodes = nodes
        self.distance = distance
        self.isEdge = isEdge
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ListEntity):
            return False
        return (sorted(self.nodes) == sorted(other.nodes))
    
if __name__ == '__main__':
    
    embedding_path = sys.argv[2]
    edgelist_path = sys.argv[1]
    embedding_name = sys.argv[2].split('/')[1]
    
    evaluation_path = 'evaluation_result/' + '/'.join(edgelist_path.split('/')[:-1]) + '/average_error_link_prediction.csv'
    if not os.path.exists(evaluation_path):
        os.makedirs('/'.join(evaluation_path.split('/')[:-1]), exist_ok=True)
        with open(evaluation_path, 'w') as file:
            file.write("\"graph\",\"embedder\",\"f_score\"\n")
    
    # get the similarity metric
    with open('/'.join(sys.argv[2].split('/')[:2]) + '/README.md', 'r') as file:
        sim_metric_str = file.read()
        sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
        module = importlib.import_module('embedding.similarity_metric')
        similarity_metric = getattr(module, sim_metric_str)
    
    averageError = AverageErrorLinkPrediction(similarity_metric)
    result = averageError.evaluate_embedding(embedding_path=embedding_path, 
                                                    edgelist_path=edgelist_path)
    
    with open(evaluation_path, 'a') as file:
        file.write("\"" + edgelist_path + '\",\"' + embedding_name + '\",' + str(result[2]) + '\n')