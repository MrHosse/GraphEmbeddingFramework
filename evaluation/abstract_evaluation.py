from abc import ABC, abstractmethod

class AbstractEvaluation(ABC):
    """
    Abstract interface for evaluation methods
    """
    
    def __init__(self, similarity_metric):
        """
        Initialize the evaluation method using a similarity metric (see similarity_metric.py)
        """
        self.similarity_metric = similarity_metric
    
    @abstractmethod
    def evaluate_embedding(self, embedding_path, edgelist_path):
        """
        Evaluate an embedding based on the respective edgelist
        """
        pass