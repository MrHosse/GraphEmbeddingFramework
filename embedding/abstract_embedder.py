from abc import ABC, abstractmethod
import os


class AbstractEmbedder(ABC):
    """
    inteface for embedding classes
    """

    def __init__(self):
        self._name = None
        self._filename = None
        self._embpath = None
        self._evlpath = None
        self.similarity_metric = None

    @abstractmethod
    def calculate_layout(self, source_graph):
        """
        calculate the layout of a given graph and save the positions of the nodes

        Args:
            source_graph: the path of the given data 
        """
        pass
    
    def save_info(self):
        if not os.path.exists(self._embpath + 'README.md'):
            with open(self._embpath + 'README.md', 'w') as f:
                f.write(self.similarity_metric.__name__)