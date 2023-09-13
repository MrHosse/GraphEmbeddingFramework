from abc import ABC, abstractmethod
import numpy
import math

class AbstractSimilarityMetric(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    def distance(vector1, vector2):
        pass
    
class EuclidianDistance(AbstractSimilarityMetric):
    def __init__(self) -> None:
        super().__init__()
        
    def distance(vector1, vector2):
        return math.dist(vector1, vector2)
    
class InnerProduct(AbstractSimilarityMetric):
    def __init__(self) -> None:
        super().__init__()
        
    def distance(vector1, vector2):
        return numpy.inner(vector1, vector2)