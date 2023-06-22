from embedding.embedding_interface import EmbeddingInterface
import networkx as nx

class Spring(EmbeddingInterface):

    def __init__(self):
        self._name = 'Fruchterman-Reingold'
        
    def calculate_layout(self, source_graph):
        
        graph = nx.read_edgelist(source_graph)

        layout = nx.spring_layout(graph)
        nodePos = list()
        for value in layout.values():
            nodePos.append(list(value))
        
        return nodePos
    