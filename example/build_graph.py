import networkx as nx
import os
import math

if __name__ == '__main__':
    
    # 1st graph group: 5 block of 10, 50 nodes overall, 100% chance of connectivity within every block and 0% between distinct blocks
    # 2nd graph group: 50 nodes with 50% chance of connectivity between every node pair
    graph_groups = [[1.0,0.0],[0.5,0.5]]
    
    for groups in graph_groups:
        in_group = groups[0]
        btw_group = groups[1]
        
        save_path = f'example/data/input_data/5_10_graphs_{in_group}g_{btw_group}ng'
        os.makedirs(save_path, exist_ok=True)
    
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
            nx.write_edgelist(graph, f'{save_path}/graph_sample_{n}', data=False)
        
    
    # 3rd graph group: random geometric graphs with 50 nodes each. The radius fulfills the equation n.pi.r^2 = 1 
    save_path = 'example/data/input_data/geometric_graphs'
    os.makedirs(save_path, exist_ok=True)
    
    nodes = 50
    radius = math.sqrt((1 / nodes) * (1 / math.pi))
    
    # 50 graphs
    for n in range(50):
        graph = nx.DiGraph(nx.random_geometric_graph(n=nodes, radius=radius))
        graph.to_directed()
        nx.write_edgelist(graph, f'{save_path}/graph_sample_{n}', data=False)

    
    # 4th graph group: 5 blocks with 6, 8, 10, 12 and 14 nodes, 50 nodes overall, 100% chance of connectivity within every block and 0% between distinct blocks
    graph_groups = [[1.0,0.0]]
    
    for groups in graph_groups:
        in_group = groups[0]
        btw_group = groups[1]
        
        save_path = f'example/data/input_data/irreg_block_graphs_{in_group}g_{btw_group}ng'
        os.makedirs(save_path, exist_ok=True)
    
        # 5 groups of 10
        sizes = [6, 8, 10, 12, 14]
    
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
            nx.write_edgelist(graph, f'{save_path}/graph_sample_{n}', data=False)
    
       
    # solo graph: Zachary’s Karate Club graph
    graph = nx.karate_club_graph()
    save_path = 'example/data/input_data/karate_club'
    nx.write_edgelist(graph, save_path, data=False)