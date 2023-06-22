from embedding.embedding_interface import EmbeddingInterface

from gem.embedding.lap import LaplacianEigenmaps
from gem.utils import graph_util

class LapEig(EmbeddingInterface):
    
    def __init__(self):
        self._name = 'LaplacianEigenmaps'
        
    def calculate_layout(self, source_graph, dim=2):
        
        graph = graph_util.loadGraphFromEdgeListTxt(source_graph, directed=True)
        graph = graph.to_directed()
        
        lapEig = LaplacianEigenmaps(d=dim)
        model = lapEig.learn_embedding(graph=graph, is_weighted=True, no_python=True)
        return model