from abc import ABC, abstractmethod

class AbstractEmbedder(ABC):
    """
    inteface for embedding classes
    """

    @abstractmethod
    def calculate_layout(self, source_graph):
        """
        calculate the layout of a given graph and save the positions of the nodes

        Args:
            source_graph: the path of the given data 
        """
        pass
    
    @abstractmethod
    def create_run(inputs):
        pass