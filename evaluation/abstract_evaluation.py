from abc import ABC, abstractmethod

class AbstractEvaluation(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def evaluate_embedding(self, embedding_path, edgelist_path):
        pass