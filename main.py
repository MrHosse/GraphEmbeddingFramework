import os
import run
import shutil
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
    
    #run.use_cores(1)
    
    input = 'data/input_data'
    embedding_result = 'data/embedding_result'
    evaluation_result = 'data/evaluation_result'
    output = 'data/output'
    
    embeddings = list()
    embeddings.append(Spring)
    embeddings.append(KamadaKawai)
    embeddings.append(Node2Vec)
    embeddings.append(Struc2Vec)
    embeddings.append(Verse)
    
    os.makedirs(embedding_result, exist_ok=True)
    
    run.group('layout')
    for embedding in embeddings:
        embedding.create_run(getFiles(input), input, embedding_result)
    
    evaluations = {
        'average_error_link_prediction': ['EuclidianDistance', 'InnerProduct'],
        'precision_at_k_link_prediction': ['EuclidianDistance', 'InnerProduct'],
        'read_time': ['None']
    }

    similarity_metric = {
        'spring': ['EuclidianDistance'],
        'kamada_kawai': ['EuclidianDistance'],
        'node2vec': ['EuclidianDistance'],
        'struc2vec': ['EuclidianDistance'],
        'verse': ['EuclidianDistance']
    }

    for embedding_variants in os.listdir(embedding_result):
        similarity_metric[embedding_variants] = similarity_metric[embedding_variants.split(' ')[0]]
        similarity_metric[embedding_variants].append('None')
    
    os.makedirs(evaluation_result, exist_ok=True)
    
    run.group('evaluation')
    for embedding in similarity_metric.keys():
        for evaluation in evaluations.keys():
            run.add(
                f"evaluate {evaluation}:{embedding}",
                f"python evaluation/{evaluation}.py \"{embedding_result}/[[embedded_graph]]\" [[sim_metric]]",
                {'embedded_graph': ['/'.join(path.split('/')[2:]) for path in getFiles(f'{embedding_result}/{embedding}')],
                'sim_metric': list(set(similarity_metric[embedding]) & set(evaluations[evaluation]))},
                stdout_file=f'{evaluation_result}/[[embedded_graph]]/[[sim_metric]]/{evaluation}.csv',
            )

    run.run()
    
    if (os.path.exists('embedding/node2vec/temp')): shutil.rmtree('embedding/node2vec/temp')
    if (os.path.exists('embedding/struc2vec/struc2vec_exe/temp')): shutil.rmtree('embedding/struc2vec/struc2vec_exe/temp')
    if (os.path.exists('embedding/verse/verse_exe/temp')): shutil.rmtree('embedding/verse/verse_exe/temp')
        
    os.makedirs(output, exist_ok=True)
    graph_groups = os.listdir(input)
    embeddings = [path for path in os.listdir(evaluation_result) if os.path.isdir(f'{evaluation_result}/{path}')]
    all_data_frame = []
    for graph_group in graph_groups:
        #data_frame = []
        for embedding in embeddings:
            files = getFiles(f'{evaluation_result}/{embedding}/{graph_group}')
            
            for file in [file for file in files if file.endswith('.csv')]:
                df = pandas.read_csv(file)
                #data_frame.append(df)
                all_data_frame.append(df)
        #if data_frame:
            #result = pandas.concat(data_frame)
            #result.to_csv(f'{output}/{graph_group}.csv', index=False)
    if all_data_frame:
        result = pandas.concat(all_data_frame)
        result.to_csv(f'{output}/all_graphs.csv', index=False)