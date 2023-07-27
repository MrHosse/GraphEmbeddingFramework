from abc import ABC, abstractmethod
import math
import statistics as stat

class AbstractEmbedder(ABC):
    """
    inteface for embedding classes
    """

    def __init__(self):
        self._name = None
        self._filename = None
        self._embpath = None
        self._evlpath = None

    @abstractmethod
    def calculate_layout(self, source_graph):
        """
        calculate the layout of a given graph and save the positions of the nodes

        Args:
            source_graph: the path of the given data 
        """
        
    def calculate_avg_edge_length(self, embedding, edgelist):
        emb = dict()
        with open(embedding, 'r') as embf:
            lines = embf.read().split('\n')
            for line in lines:
                if line == '': continue 
                coord = line.split(',')
                emb[int(coord[0])] = list(map(float, coord[1:]))
        
        edge_length = list()
        with open(edgelist, 'r') as edgelistf:
            edges = edgelistf.read().split('\n')
            for edge in edges:
                if edge == '': continue 
                ed = edge.split(' ')
                edge_length.append(math.dist(emb[int(ed[0])], emb[int(ed[1])]))
        
        return stat.fmean(edge_length)