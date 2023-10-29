from abc import ABC, abstractmethod
import numpy
import math

class AbstractSimilarityMetric(ABC):
    """
    This is an interface for similarity metrics.
    """
    def __init__(self) -> None:
        super().__init__()
        
    def distance(vector1, vector2):
        """
        Each similarity metric must implement a distance function, which calculates
        the distanse between 2 nodes, based on the coordination vectors
        
        Returns:
            A comparable value (e.g. float)
        """
        pass
    
class EuclidianDistance(AbstractSimilarityMetric):
    """
    The distance between 2 nodes based on their distance in euclidian geometry
    """
    def __init__(self) -> None:
        super().__init__()
        
    def distance(vector1, vector2):
        return math.dist(vector1, vector2)
    
class InnerProduct(AbstractSimilarityMetric):
    """
    The distance between 2 nodes based on their inner product
    """
    def __init__(self) -> None:
        super().__init__()
        
    def distance(vector1, vector2):
        return -numpy.inner(vector1, vector2)