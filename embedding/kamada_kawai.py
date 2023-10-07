import sys
import os
import time

from abstract_embedder import AbstractEmbedder
import networkx as nx
from similarity_metric import EuclidianDistance

class KamadaKawai(AbstractEmbedder):

    def __init__(self):
        self._name = 'Kamada-Kawai'
        self._filename = 'embedding/kamada_kawai.py'
        self._embpath = 'embedding_result/kamada_kawai/'
        self._evlpath = 'evaluation_result/'
        self.similarity_metric = EuclidianDistance

    def calculate_layout(self, source_graph):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.kamada_kawai_layout(graph)
        
        os.makedirs(self._embpath + '/'.join(source_graph.split('/')[:-1]), exist_ok=True)
        
        output = ""
        for key in layout.keys():
            values = layout[key]
            value_str = ','.join(str(value) for value in values)
            line = f"{key},{value_str}\n"
            output += line
        return output
            
        
if __name__ == '__main__':
    kamada_kawai = KamadaKawai()
    
    print(kamada_kawai.calculate_layout(source_graph=sys.argv[1]))