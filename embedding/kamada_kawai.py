import sys
import os
import time

from abstract_embedder import AbstractEmbedder
import networkx as nx

class KamadaKawai(AbstractEmbedder):

    def __init__(self):
        self._name = 'Kamada-Kawai'
        self._filename = 'embedding/kamada_kawai.py'
        self._embpath = 'embedding_result/kamada_kawai/'
        self._evlpath = 'evaluation_result/'

    def calculate_layout(self, source_graph):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.kamada_kawai_layout(graph)
        
        os.makedirs(self._embpath + 'input_data', exist_ok=True)
        with open(self._embpath + sys.argv[1], 'w') as file:
            output = ""
            for key in layout.keys():
                values = layout[key]
                value_str = ','.join(str(value) for value in values)
                line = f"{key},{value_str}\n"
                output += line
            file.write(output)
            
        
if __name__ == '__main__':
    kamada_kawai = KamadaKawai()
    
    t0 = time.time()
    kamada_kawai.calculate_layout(source_graph=sys.argv[1])
    t1 = time.time()
    
    os.makedirs(kamada_kawai._evlpath + 'input_data', exist_ok=True)
    with open(kamada_kawai._evlpath + sys.argv[1], 'a') as file:
        file.write(kamada_kawai._name + ',')
        file.write(str(t1 - t0) + ',')
        file.write(str(kamada_kawai.calculate_avg_edge_length(
            edgelist=sys.argv[1], 
            embedding=(kamada_kawai._embpath + sys.argv[1]))) + '\n')