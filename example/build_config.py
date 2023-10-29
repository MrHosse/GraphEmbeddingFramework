import json
import os

if __name__ == '__main__':
    
    savepath = 'example/data/config'
    os.makedirs(savepath, exist_ok=True)
    
    # configuration for running the experiments
    main_config = {
        'embeddings': ['Spring', 'Node2Vec', 'Struc2Vec', 'Verse'],
        'evaluations': {
            'average_error_link_prediction': ['EuclidianDistance', 'InnerProduct'],
            'precision_at_k_link_prediction': ['EuclidianDistance', 'InnerProduct'],
            'read_time': ['None']
        },
        'similarity_metrics': {
            'spring': ['EuclidianDistance', 'None'],
            'node2vec': ['EuclidianDistance', 'None'],
            'struc2vec': ['EuclidianDistance', 'None'],
            'verse': ['EuclidianDistance', 'InnerProduct', 'None']
        },
        'csv_per_dir': True,
        'num_parallel_runs': 4
    }
    
    with open(f'{savepath}/main.json', 'w') as main_config_file:
        json.dump(main_config, main_config_file, indent=4)
        
    
    # configuration for node2vec embedder: 2 different dimensions: default (2) and 12
    node2vec_config = {
        'dim': ['default', 12]
    }
    with open(f'{savepath}/node2vec.json', 'w') as node2vec_config_file:
        json.dump(node2vec_config, node2vec_config_file, indent=4)