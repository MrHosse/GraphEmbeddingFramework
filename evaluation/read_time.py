import sys
from abstract_evaluation import AbstractEvaluation

class ReadTime(AbstractEvaluation):
    """
    This evaluation metric reads the time from the embedding path
    """
    def __init__(self, argv) -> None:
        super().__init__(argv)
        
    def evaluate_embedding(self):
        embedding_path = self.embedding_path
        
        with open(embedding_path, 'r') as embedding:
            return embedding.readline().split(' ')[1]
    
if __name__ == '__main__':
    
    readTime = ReadTime(sys.argv)
    time = readTime.evaluate_embedding()
    
    output = readTime.get_output_line('time', time)
    
    print(output)