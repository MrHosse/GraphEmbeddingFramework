import sys
from abstract_evaluation import AbstractEvaluation

class AverageErrorLinkPrediction(AbstractEvaluation):
    """
    Based on an embedding and an edgelist, this evaluation metric calculates the optimal
    edge length, for which the f_score is the highest.
    f_score is the harmonic mean of precision and recall.
    """
    
    def __init__(self, argv) -> None:
        super().__init__(argv)
        
    def evaluate_embedding(self):
        embedding_path = self.embedding_path
        similarity_metric = self.similarity_metric
        
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
    """
    Instances of this class are used in the top class to sort node pairs easier 
    """
    def __init__(self, nodes, distance, isEdge):
        self.nodes = nodes
        self.distance = distance
        self.isEdge = isEdge
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ListEntity):
            return False
        return (sorted(self.nodes) == sorted(other.nodes))
    
if __name__ == '__main__':
    
    averageError = AverageErrorLinkPrediction(sys.argv)
    result = averageError.evaluate_embedding()
    
    output = averageError.get_output_line('f_score', result[2])
    
    print(output)