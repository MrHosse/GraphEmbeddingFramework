import networkx as nx

if __name__ == '__main__':
    sizes = [10 for _ in range(5)]
    probs1 = [[0 for _ in range(5)] for _ in range(5)]
    probs2 = [[0.2 for _ in range(5)] for _ in range(5)]
    probs3 = [[0.2 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        probs1[i][i] = 1
        probs2[i][i] = 1
        probs3[i][i] = 0.8
        
    nx.write_edgelist(nx.stochastic_block_model(sizes, probs1, directed=True), 'input_data/1g0ng', data=False)
    nx.write_edgelist(nx.stochastic_block_model(sizes, probs2, directed=True), 'input_data/1g02ng', data=False)
    nx.write_edgelist(nx.stochastic_block_model(sizes, probs3, directed=True), 'input_data/08g02ng', data=False)
    
    
    
    