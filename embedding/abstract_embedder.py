from abc import ABC, abstractmethod

class AbstractEmbedder(ABC):
    """
    inteface for embedding classes
    """
    
    @abstractmethod
    def create_run(inputs, source_dir, target_dir):
        """
        Reads the config data and sets the needed parameters for the embedding.
        Consequently creates a run for this embedding.
        
        Args:
            inputs - list of string: a list of source graphs which should be embedded.
            source_dir - string: path to the directory, where the source graphs are placed.
            target_dir - string: path to the directory, where the results should be saved.
        """
        pass
    
    @abstractmethod
    def calculate_layout(self, source_graph):
        """
        Calculate the layout of a given graph and save the positions of the nodes

        Args:
            source_graph - string: the path of the given data 
        Returns:
            string
            The embedding of source_graph.
            The first line contains the path to the edgelist followed by the 
            needed time for calculation separated by whitespace (' ').
            The remaining lines consist of the name of the nodes followed by 
            their coordination separated by comma (',').
        """
        pass
    