import sys
from abstract_evaluation import AbstractEvaluation

class ReadTime(AbstractEvaluation):
    
    def __init__(self, similarity_metric) -> None:
        super().__init__(similarity_metric)
        
    def evaluate_embedding(self, embedding_path):
        with open(embedding_path, 'r') as embedding:
            return embedding.readline().split(' ')[1]
    
if __name__ == '__main__':
    
    embedding_path = sys.argv[1]
    with open(embedding_path, 'r') as embedding:
        edgelist = embedding.readline().split(' ')[0]
        group = edgelist.split('/')[2]
    embedding = embedding_path.split('/')[2]
    
    readTime = ReadTime(None)
    time = readTime.evaluate_embedding(embedding_path=embedding_path)
    
    output = "edgelist,group,embedder,similarity_metric,type,value\n"
    output += f'{edgelist},{group},{embedding},None,time,{time}'
    
    print(output)