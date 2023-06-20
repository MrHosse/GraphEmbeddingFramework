from abc import ABC, abstractmethod
import os

class EmbeddingInterface(ABC):
    """
    inteface for embedding classes
    """

    def __init__(self):
        self._name = None

    @abstractmethod
    def calculate_layout(self, source_graph):
        """
        calculate the layout of a given graph and save the positions of the nodes

        Args:
            source_graph: the path of the given data 
        """
