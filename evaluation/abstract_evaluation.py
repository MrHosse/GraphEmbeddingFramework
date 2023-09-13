from abc import ABC, abstractmethod

class AbstractEvaluation(ABC):
    def __init__(self, similarity_metric):
        self.similarity_metric = similarity_metric
    
    @abstractmethod
    def evaluate_embedding(self, embedding_path, edgelist_path):
        pass