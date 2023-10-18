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
        "similarity_metrics": {
            'spring': ['EuclidianDistance'],
            'node2vec': ['EuclidianDistance'],
            'struc2vec': ['EuclidianDistance'],
            'verse': ['EuclidianDistance', 'InnerProduct']
        }
    }
    
    with open(f'{savepath}/main.json', 'w') as main_config_file:
        json.dump(main_config, main_config_file, indent=4)
        
    
    # configuration for spring embedder: 2 different dimensions: default (2) and 12
    spring_config = {
        'dim': ['default', 12]
    }
    with open(f'{savepath}/spring.json', 'w') as spring_config_file:
        json.dump(spring_config, spring_config_file, indent=4)