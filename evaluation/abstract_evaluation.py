from abc import ABC, abstractmethod
import sys
import importlib
import os

class AbstractEvaluation(ABC):
    """
    Abstract interface for evaluation methods
    """
    
    def __init__(self, argv):
        """
        Initializes the evaluation method using arguments passed in command line and
        sets the attributes for evaluation class
        """
        embedding_path = argv[1]
        with open(embedding_path, 'r') as embedding:
            edgelist = embedding.readline().split(' ')[0]
            group = edgelist.split('/')[2]
        sim_metric_str = argv[2]
        embedding = embedding_path.split('/')[2]
    
        # get the similarity metric
        if sim_metric_str == 'None':
            similarity_metric = None
        else:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
            module = importlib.import_module('evaluation.similarity_metric')
            similarity_metric = getattr(module, sim_metric_str)
        
        self.embedding_path = embedding_path
        self.similarity_metric = similarity_metric
        self.embedding = embedding
        self.edgelist = edgelist
        self.group = group
    
    def get_output_line(self, type, value):
        """
        From a given type and value computes an output line in the format:
        "edgelist,group,embedder,similarity_metric,type,value"
        
        Args:
            type - string: the type of the value
            value - float: the value
            
        Returns:
            A line of output
        """
        return f'{self.edgelist},{self.group},{self.embedding},{self.similarity_metric.__name__ if self.similarity_metric else self.similarity_metric},{type},{value}\n'
    
    @abstractmethod
    def evaluate_embedding(self):
        """
        Evaluate an embedding based on the respective edgelist
        """
        pass