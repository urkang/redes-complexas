import networkx as nx
from random import randint


# compute the number of shortest paths that pass through each node. Returns dict
def num_spaths(graph):
    n_spaths = dict.fromkeys(graph, 0.0)
    spaths = dict(nx.all_pairs_shortest_path(graph))

    for source in spaths:
        for path in spaths[source].items():
            for node in path[1][1:]:  # ignore first element (source == node)
                n_spaths[node] += 1  # this path passes through `node`

    return n_spaths


# removes a random node and cascades
def remove_random(graph, initial_loads, tolerance):
    nodes = list(graph.nodes())
    index = randint(0, len(nodes) - 1)
    graph.remove_node(nodes[index])
    print("Node Removed")
    stable = False
    while not stable:
        current_load = num_spaths(graph)
        for node_load in current_load.items():
            node = node_load[0]
            load = node_load[1]
            if load > (1 - tolerance) * initial_loads[node]:
                graph.remove_node(node)
                print("Node Removed by cascading")
                break
        stable = True


# removes a node by highest degree and cascades
def remove_highest_degree(graph, initial_loads, tolerance):
    nodes = list(graph.nodes())
    degrees = graph.degree()
    index = max(degrees, key=degrees.get)
    graph.remove_node(nodes[index])
    print("Node Removed")
    stable = False
    while not stable:
        current_load = num_spaths(graph)
        for node_load in current_load.items():
            node = node_load[0]
            load = node_load[1]
            if load > (1 - tolerance) * initial_loads[node]:
                graph.remove_node(node)
                print("Node Removed by cascading")
                break
        stable = True


# removes a node by highest load and cascades
def remove_highest_load(graph, initial_loads, tolerance):
    nodes = list(graph.nodes())
    index = max(initial_loads, key=initial_loads.get)
    graph.remove_node(nodes[index])
    print("Node Removed")
    stable = False
    while not stable:
        current_load = num_spaths(graph)
        for node_load in current_load.items():
            node = node_load[0]
            load = node_load[1]
            if load > (1 - tolerance) * initial_loads[node]:
                graph.remove_node(node)
                print("Node Removed by cascading")
                break
        stable = True


# simulates the removal of a node and calculates the cascading effect
def simulate(graph, tolerance, removal_function, filename):
    initial_loads = num_spaths(graph)
    removal_function(graph.copy(), initial_loads, tolerance)

    component_sizes = list(map(lambda sg: sg.size(), list(nx.connected_component_subgraphs(graph))))
    N_prime = max(component_sizes) if len(component_sizes) > 0 else 0
    G = N_prime / N if N != 0 else 0

    print("Tolerance", tolerance)
    print("Global size: ", graph.size())
    print("Giant Component size: ", N_prime)
    print("G: ", G)

    with open(filename + ".txt", "w") as f:
        f.write(str([tolerance, graph.size(), N_prime, G]))
    return [tolerance, graph.size(), N_prime, G]


n = 5000  # number of nodes
m = 2  # number of edges for the preferential attachment
graph = nx.barabasi_albert_graph(n, m)  # make a random scale-free graph using barabasi_albert model

component_sizes = list(map(lambda sg: sg.size(), list(nx.connected_component_subgraphs(graph))))
N = max(component_sizes) if len(component_sizes) > 0 else 0

# run the simulation for each tolerance value
simulation_results = []
for tolerance in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    print("Simulating with tolerance: ", tolerance)
    result = simulate(graph.copy(), tolerance, remove_random, "scale_free_5000_removed_by_random")
    # result = simulate(graph.copy(), tolerance, remove_highest_degree, "scale_free_5000_removed_by_highest_degree")
    # result = simulate(graph.copy(), tolerance, remove_highest_load, "scale_free_5000_removed_by_highest_load")
    simulation_results.append(result)

print(simulation_results)





