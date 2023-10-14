import os
import run
import pandas
from embedding.spring.spring import Spring
from embedding.kamada_kawai.kamada_kawai import KamadaKawai
from embedding.node2vec.node2vec import Node2Vec
from embedding.struc2vec.struc2vec import Struc2Vec
from embedding.verse.verse import Verse

def getFiles(path) -> list:
    result = []
    
    if os.path.isfile(path) and path.split('/')[-1] != 'README.md': return result.append(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isfile(f) and filename != 'README.md': 
                result.append(f)
            elif os.path.isdir(f) and filename != 'README.md':
                result.extend(getFiles(f))
    
    return result

if __name__ == "__main__":
    
    input = 'input_data'

    """ if os.path.exists('embedding/verse_exe/temp'):
        shutil.rmtree('embedding/verse_exe/temp')
    if os.path.exists('embedding/struc2vec_exe/temp'):
        shutil.rmtree('embedding/struc2vec_exe/temp') """
    
    embeddings = list()
    embeddings.append(Spring)
    embeddings.append(KamadaKawai)
    embeddings.append(Node2Vec)
    embeddings.append(Struc2Vec)
    embeddings.append(Verse)
    
    os.makedirs('embedding_result', exist_ok=True)
    
    run.group('layout')
    for embedding in embeddings:
        embedding.create_run(getFiles(input))
    
    evaluations = list()
    evaluations.append('average_error_link_prediction')
    evaluations.append('precision_at_k_link_prediction')
    evaluations.append('read_time')

    similarity_metric = {
        'spring': ['EuclidianDistance'],
        'kamada_kawai': ['EuclidianDistance'],
        'node2vec': ['EuclidianDistance'],
        'struc2vec': ['EuclidianDistance'],
        'verse': ['EuclidianDistance']
    }

    os.makedirs('evaluation_result', exist_ok=True)
    
    run.group('evaluation')
    for embedding in similarity_metric.keys():
        run.add(
            f"evaluate {embedding}",
            "python evaluation/[[evaluation]].py embedding_result/[[embedded_graph]] " + ' '.join(similarity_metric[embedding]),
            {'evaluation': evaluations,
            'embedded_graph': ['/'.join(path.split('/')[1:]) for path in getFiles(f'embedding_result/{embedding}')]},
            stdout_file='evaluation_result/[[embedded_graph]]/[[evaluation]].csv',
        )
        
    run.run()
    
    os.makedirs('output', exist_ok=True)
    graph_groups = [path for path in os.listdir(input) if os.path.isdir(f'{input}/{path}')]
    embeddings = [f'evaluation_result/{path}' for path in os.listdir('evaluation_result') if os.path.isdir(f'evaluation_result/{path}')]
    all_data_frame = []
    for graph_group in graph_groups:
        data_frame = []
        for embedding in embeddings:
            files = getFiles(f'{embedding}/{input}/{graph_group}')
            for file in [file for file in files if file.endswith('.csv')]:
                df = pandas.read_csv(file)
                data_frame.append(df)
                all_data_frame.append(df)
        if data_frame:
            result = pandas.concat(data_frame)
            result.to_csv(f'output/{graph_group}.csv', index=False)
    if all_data_frame:
        result = pandas.concat(all_data_frame)
        result.to_csv('output/all_graphs.csv')