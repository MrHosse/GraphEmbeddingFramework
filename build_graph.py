import networkx as nx
import random
import os

if __name__ == '__main__':
    
    save_path = 'input_data/5_10_graphs'
    os.makedirs(save_path, exist_ok=True)
    with open(save_path + '/README.md', 'w') as readmef:
        readmef.write(
            "The graphs in this folder contain 5 groups of 10 nodes.\n" +
            "Probility of edges in a group: a rondom in [0.75, 1.0]\n" + 
            "Probility of edges between groups: a random in [0.0, 0.25]"
            )
    
    # 10 groups of 50
    sizes = [10 for _ in range(5)]
    
    # 50 graphs
    for n in range(50):
        probs = []
        for i in range(5):
            prob_g_i = []
            for j in range(5):
                if i == j:
                    prob_g_i.append(random.uniform(0.75, 1))
                else:
                    prob_g_i.append(random.uniform(0, 0.25))
            probs.append(prob_g_i)
        graph = nx.stochastic_block_model(sizes=sizes, p=probs, directed=True)
        nx.write_edgelist(graph, save_path + '/graph_sample_' + str(n), data=False)
        
    
    
    save_path = 'input_data/geometric_graphs'
    os.makedirs(save_path, exist_ok=True)
    radius = 0.1
    with open(save_path + '/README.md', 'w') as readmef:
        readmef.write(
            "The graphs in this folder contain random geometric graphs\n" +
            "2 Edges are connected, if they are closer than " + str(radius)
            )
        
    # 50 graphs
    for n in range(50):
        graph = nx.Graph(nx.random_geometric_graph(n=50, radius=radius))
        nx.write_edgelist(graph, save_path + '/graph_sample_' + str(n), data=False)
    