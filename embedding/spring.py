import sys
import os

from abstract_embedder import AbstractEmbedder
import networkx as nx
from similarity_metric import EuclidianDistance
    
class Spring(AbstractEmbedder):

    def __init__(self):
        self._name = 'Fruchterman-Reingold'
        self._filename = 'embedding/spring.py'
        self._embpath = 'embedding_result/spring/'
        self._evlpath = 'evaluation_result/'
        self.similarity_metric = EuclidianDistance
        
    def calculate_layout(self, source_graph):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.spring_layout(graph)
        
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        
        with open(self._embpath + source_graph, 'w') as file:
            output = ""
            for key in layout.keys():
                values = layout[key]
                value_str = ','.join(str(value) for value in values)
                line = f"{key},{value_str}\n"
                output += line
            file.write(output)
        
        
if __name__ == '__main__':
    spring = Spring()
    
    if not os.path.exists(spring._embpath + sys.argv[1]):
        spring.calculate_layout(source_graph=sys.argv[1])
    
    spring.save_info()
    
    # os.makedirs(spring._evlpath + 'input_data', exist_ok=True)
    # with open(spring._evlpath + sys.argv[1], 'w') as file:
    #     file.write('embedding,time,avg edge length\n')
        
    #     file.write(spring._name + ',')
    #     file.write(str(t1 - t0) + ',')
    #     file.write(str(spring.calculate_avg_edge_length(
    #         edgelist=sys.argv[1], 
    #         embedding=(spring._embpath + sys.argv[1]))) + '\n')
    