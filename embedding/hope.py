import sys

from abstract_embedder import AbstractEmbedder

import networkx as nx
import numpy as np
import scipy.sparse.linalg as lg

from gem.embedding.hope import HOPE
from gem.utils import graph_util

class Hope(AbstractEmbedder):
    
    def __init__(self):
        self._name = 'HOPE'
        self._filename = 'embedding/hope.py'
        
    def calculate_layout(self, source_graph, dim=4, beta=0.01):
        
        graph = graph_util.loadGraphFromEdgeListTxt(source_graph, directed=True)
        graph = graph.to_directed()
        
        A = nx.to_numpy_matrix(graph)
        m_g = np.eye(len(graph.nodes)) - beta * A
        m_l = beta * A
        S = np.dot(np.linalg.inv(m_g), m_l)

        u, s, vt = lg.svds(S, k=dim // 2)
        X1 = np.dot(u, np.diag(np.sqrt(s)))
        X2 = np.dot(vt.T, np.diag(np.sqrt(s)))
        X = np.concatenate((X1, X2), axis=1)
        
        output = ""
        for i in range(len(X)):
            output += f"{str(i)},{','.join(str(value) for value in X[i])}\n"
        
        print(output)

        #p_d_p_t = np.dot(u, np.dot(np.diag(s), vt))
        #eig_err = np.linalg.norm(p_d_p_t - S)
        
if __name__ == '__main__':
    hope = Hope()
    hope.calculate_layout(source_graph=sys.argv[1])        
        