from embedding.embedding_interface import EmbeddingInterface

from gem.embedding.hope import HOPE
from gem.utils import graph_util

class Hope(EmbeddingInterface):
    
    def __init__(self):
        self._name = 'HOPE'
        
    def calculate_layout(self, source_graph, dim=4, beta=0.01):
        
        graph = graph_util.loadGraphFromEdgeListTxt(source_graph, directed=True)
        graph = graph.to_directed()
        
        hope = HOPE(d=dim, beta=beta)
        model = hope.learn_embedding(graph=graph, is_weighted=True, no_python=True)
        return model