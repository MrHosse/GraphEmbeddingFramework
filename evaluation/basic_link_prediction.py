import math
import sys

from abstract_evaluation import AbstractEvaluation

class BasicLinkPrediction(AbstractEvaluation):
    
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
        n = len(nodes)
        non_edges = ((n * (n - 1)) / 2) - m
        
        optimal_tp = -1
        optimal_positive = -1
        optimal_parameter = -1
        
        for i in range(len(sorted_node_pairs)):
            pair = node_pairs[i]
            if (pair.isEdge): left_edges += 1
            else: left_non_edges += 1
            
            # calculate the harmonic mean of edge ration on left side and non edge ratio on right side
            edge_ratio = left_edges / (left_edges + left_non_edges)
            non_edge_ratio = 1 if (non_edges - left_non_edges + m - left_edges) == 0 else (non_edges - left_non_edges) / (non_edges - left_non_edges + m - left_edges)
            current_parameter = (2 * edge_ratio * non_edge_ratio) / (edge_ratio + non_edge_ratio)
            
            if (current_parameter > optimal_parameter):
                optimal_parameter = current_parameter
                optimal_tp = left_edges
                optimal_positive = i + 1
        
        precision = (optimal_tp) / (optimal_positive)
        recall = (optimal_tp) / (m)
        f_score = (2 * precision * recall) / (precision + recall)
        
        return [precision, recall, f_score] 
        
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
    
    edgelist_path = sys.argv[1]
    embedding_path = sys.argv[2]
    evaluation_path = 'evaluation_result/' + edgelist_path.split('/')[-1]
    
    basicLinkPrediction = BasicLinkPrediction()
    result = basicLinkPrediction.evaluate_embedding(embedding_path=embedding_path, 
                                                    edgelist_path=edgelist_path)
    
    with open(evaluation_path, 'w') as evalf:
        evalf.write(
            "Evaluation result using basic link prediction:\n" +
            "\tprecision: " + str(result[0]) + '\n' +
            "\trecall: " + str(result[1]) + '\n' + 
            "\tf_score: " + str(result[2]) + '\n'
        )