import networkx as nx
import os
import math

if __name__ == '__main__':
    
    graph_groups = [[1.0,0.0],[0.75,0.25],[0.5,0.5]]
    
    for groups in graph_groups:
        in_group = groups[0]
        btw_group = groups[1]
        
        save_path = 'input_data/5_10_graphs_' + str(in_group) + 'g_' + str(btw_group) + 'ng'
        os.makedirs(save_path, exist_ok=True)
        with open(save_path + '/README.md', 'w') as readmef:
            readmef.write(
                "The graphs in this folder contain 5 groups of 10 nodes.\n" +
                "Probility of edges in a group: " + str(in_group) + "\n" + 
                "Probility of edges between groups: " + str(btw_group)
            )
    
        # 5 groups of 10
        sizes = [10 for _ in range(5)]
    
        # 50 graphs
        for n in range(50):
            probs = []
            for i in range(5):
                prob_g_i = []
                for j in range(5):
                    if i == j:
                        prob_g_i.append(in_group)
                    else:
                        prob_g_i.append(btw_group)
                probs.append(prob_g_i)
            graph = nx.stochastic_block_model(sizes=sizes, p=probs, directed=True)
            nx.write_edgelist(graph, save_path + '/graph_sample_' + str(n), data=False)
        
    
    
    save_path = 'input_data/geometric_graphs'
    os.makedirs(save_path, exist_ok=True)
    radius = math.sqrt(0.2 * (1 / math.pi))
    with open(save_path + '/README.md', 'w') as readmef:
        readmef.write(
            "The graphs in this folder contain random geometric graphs\n" +
            "2 Edges are connected, if they are closer than " + str(radius)
            )
        
    # 50 graphs
    for n in range(50):
        graph = nx.DiGraph(nx.random_geometric_graph(n=50, radius=radius))
        graph.to_directed()
        nx.write_edgelist(graph, save_path + '/graph_sample_' + str(n), data=False)

    
    graph_groups = [[1.0,0.0],[0.75,0.25]]
    
    for groups in graph_groups:
        in_group = groups[0]
        btw_group = groups[1]
        
        save_path = 'input_data/irreg_block_graphs_' + str(in_group) + 'g_' + str(btw_group) + 'ng'
        os.makedirs(save_path, exist_ok=True)
        with open(save_path + '/README.md', 'w') as readmef:
            readmef.write(
                "The graphs in this folder contain.\n" +
                "Probility of edges in a group: " + str(in_group) + "\n" + 
                "Probility of edges between groups: " + str(btw_group)
            )
    
        # 5 groups of 10
        sizes = [8, 9, 10, 11, 12]
    
        # 50 graphs
        for n in range(50):
            probs = []
            for i in range(5):
                prob_g_i = []
                for j in range(5):
                    if i == j:
                        prob_g_i.append(in_group)
                    else:
                        prob_g_i.append(btw_group)
                probs.append(prob_g_i)
            graph = nx.stochastic_block_model(sizes=sizes, p=probs, directed=True)
            nx.write_edgelist(graph, save_path + '/graph_sample_' + str(n), data=False)