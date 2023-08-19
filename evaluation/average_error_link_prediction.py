import math
import sys
import os
from abstract_evaluation import AbstractEvaluation

class AverageErrorLinkPrediction(AbstractEvaluation):
    
    def __init__(self) -> None:
        super().__init__()
        
    def evaluate_embedding(self, embedding_path, edgelist_path):
        # read the embedding
        embedding = dict()
        with open(embedding_path, 'r') as embf:
            lines = embf.read().split('\n')
            for line in lines:
                if line == '': continue
                coord = line.split(',')
                embedding[int(coord[0])] = list(map(float, coord[1:]))
        
        # read edgelist and ignore loops
        edge_list = list()
        with open(edgelist_path, 'r') as edgef:
            edges = edgef.read().split('\n')
            for edge in edges:
                if edge == '': continue
                if not edge.split(' ')[0] == edge.split(' ')[1]:
                    edge_list.append(sorted(list(map(int, edge.split(' ')))))
        
        # save all node pairs to find the optimal edge length
        nodes = sorted(list(embedding.keys()))
        node_pairs = list()
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if ([nodes[i], nodes[j]] in edge_list):
                    node_pairs.append(ListEntity(nodes=[nodes[i], nodes[j]], 
                                    distance=math.dist(embedding[nodes[i]], embedding[nodes[j]]), 
                                    isEdge=True))
                else:
                    node_pairs.append(ListEntity(nodes=[nodes[i], nodes[j]], 
                                    distance=math.dist(embedding[nodes[i]], embedding[nodes[j]]), 
                                    isEdge=False))
        
        # sort based on distance
        sorted_node_pairs = sorted(node_pairs, key=lambda x: x.distance)
        
        # find the optimal length
        left_edges = 0
        left_non_edges = 0
        m = len(edge_list)
        
        optimal_precision = -1
        optimal_recall = -1
        optimal_f_score = -1
        
        for i in range(len(sorted_node_pairs)):
            pair = sorted_node_pairs[i]
            if (pair.isEdge): left_edges += 1
            else: left_non_edges += 1
            
            
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
    
    evaluation_path = 'evaluation_result/average_error_link_prediction.csv'
    if not os.path.exists(evaluation_path):
        with open(evaluation_path, 'w') as file:
            file.write("graph,embedder,f_score\n")
    
    embedding_path = sys.argv[2]
    edgelist_path = sys.argv[1]
    embedding_name = sys.argv[2].split('/')[-3]
    
    averageError = AverageErrorLinkPrediction()
    result = averageError.evaluate_embedding(embedding_path=embedding_path, 
                                                    edgelist_path=edgelist_path)
    
    with open(evaluation_path, 'a') as file:
        file.write(edgelist_path + ',' + embedding_name + ',' + str(result[2]) + '\n')
    
    """ edgelist_path = sys.argv[1]
    embedding_path = sys.argv[2]
    evaluation_path = 'evaluation_result/' + edgelist_path.split('/')[-1]
    embedding_name = sys.argv[2].split('/')[-3]
    
    averageError = AverageErrorLinkPrediction()
    result = averageError.evaluate_embedding(embedding_path=embedding_path, 
                                                    edgelist_path=edgelist_path)
    
    keyword = 'a' if os.path.exists(evaluation_path) else 'w'
    
    with open(evaluation_path, keyword) as evalf:
        evalf.write(
            "Evaluation result using " + embedding_name + " based on average error link prediction:\n" +
            "\tprecision: " + str(result[0]) + '\n' +
            "\trecall: " + str(result[1]) + '\n' + 
            "\tf_score: " + str(result[2]) + '\n\n'
        ) """