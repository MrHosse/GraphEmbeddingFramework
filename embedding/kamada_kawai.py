import sys

from abstract_embedder import AbstractEmbedder
import networkx as nx

class KamadaKawai(AbstractEmbedder):

    def __init__(self):
        self._name = 'Kamada-Kawai'
        self._filename = 'embedding/kamada_kawai.py'

    def calculate_layout(self, source_graph):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.kamada_kawai_layout(graph)
        
        output = ""
        for key in layout.keys():
            values = layout[key]
            value_str = ','.join(str(value) for value in values)
            line = f"{key},{value_str}\n"
            output += line
            
        print(output)
        
if __name__ == '__main__':
    kamada_kawai = KamadaKawai()
    kamada_kawai.calculate_layout(source_graph=sys.argv[1])