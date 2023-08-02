import math
import sys
import os
from abstract_evaluation import AbstractEvaluation

class PrecisionAtKLinkPrediction(AbstractEvaluation):
    
    given_node = list()
    embedding = dict()
    nodes = list()
    neighbour_count = dict()
    
    def __init__(self) -> None:
        super().__init__()
    
    def distance_from_given_node(node):
        return math.dist(PrecisionAtKLinkPrediction.embedding[PrecisionAtKLinkPrediction.nodes[PrecisionAtKLinkPrediction.given_node]], 
                         PrecisionAtKLinkPrediction.embedding[PrecisionAtKLinkPrediction.nodes[node]])
    
    def evaluate_embedding(self, k, embedding_path, edgelist_path):
        # read the embedding
        embedding = dict()
        with open(embedding_path, 'r') as embf:
            lines = embf.read().split('\n')
            for line in lines:
                if line == '': continue
                coord = line.split(',')
                embedding[int(coord[0])] = list(map(float, coord[1:]))
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
                    edge_list.append(sorted(list(map(int, edge.split(' ')))))
                    neighbour_count[int(edge.split(' ')[0])] += 1
                    neighbour_count[int(edge.split(' ')[1])] += 1
        PrecisionAtKLinkPrediction.neighbour_count = neighbour_count
        
        # build a list with every node pair and sort them based on distance
        pairs = list()
        for i in range(len(nodes)):
            node_list = []
            for j in range(len(nodes)):
                if i != j: node_list.append(j)
            PrecisionAtKLinkPrediction.given_node = i
            node_list = sorted(node_list, key=PrecisionAtKLinkPrediction.distance_from_given_node)
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
    
    k = 3
    edgelist_path = sys.argv[1]
    embedding_path = sys.argv[2]
    evaluation_path = 'evaluation_result/' + edgelist_path.split('/')[-1]
    embedding_name = sys.argv[2].split('/')[-3]
    
    model = PrecisionAtKLinkPrediction()
    result = model.evaluate_embedding(embedding_path=embedding_path,
                                      edgelist_path=edgelist_path,
                                      k=k)
    
    keyword = 'a' if os.path.exists(evaluation_path) else 'w'
    
    with open(evaluation_path, keyword) as evalf:
        evalf.write(
            "Evaluation result using %s based on link prediction for k nearest nodes with k = %d:\n" % (embedding_name, k)
        )
        for key in list(result.keys()):
            evalf.write("\tnode %d: %d out of %d\n" % (key, result[key], PrecisionAtKLinkPrediction.neighbour_count[key]))
        evalf.write('\n')