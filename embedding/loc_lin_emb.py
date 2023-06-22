from embedding.embedding_interface import EmbeddingInterface

from gem.embedding.lle import LocallyLinearEmbedding
from gem.utils import graph_util

class LocLinEmb(EmbeddingInterface):
    
    def __init__(self):
        self._name = 'LocallyLinearEmbedding'
        
    def calculate_layout(self, source_graph, dim=2):
        
        graph = graph_util.loadGraphFromEdgeListTxt(source_graph, directed=True)
        graph = graph.to_directed()
        
        lle = LocallyLinearEmbedding(d=dim)
        model = lle.learn_embedding(graph=graph, is_weighted=True, no_python=True)
        return model