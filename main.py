import networkx as nx
import matplotlib.pyplot as plt


def dijkstra(graph, source):
    dist = {}
    prev = {}
    first_links = {}

    for node in graph.nodes():
        dist[node] = float('inf')
        prev[node] = None
        first_links[node] = None

    dist[source] = 0
    unvisited = list(graph.nodes())

    while unvisited:
        min_dist = float('inf')
        u = None

        for node in unvisited:
            if dist[node] < min_dist:
                min_dist = dist[node]
                u = node

        if u is None:
            break

        unvisited.remove(u)

        for v in graph.neighbors(u):
            alt = dist[u] + graph.edges[u, v]['weight']
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                if first_links[u] is not None:
                    first_links[v] = first_links[u]
                else:
                    first_links[v] = f"{u}-{v}"

    return dist, prev, first_links


# read input from file
with open('input.txt', 'r') as file:
    n, m = map(int, file.readline().split(','))
    edges = []
    for _ in range(m):
        u, v, w = file.readline().strip().split(',')
        edges.append((u, v, int(w)))

# create graph
G = nx.Graph()
G.add_weighted_edges_from(edges)

# calculate forwarding tables
forwarding_tables = nx.all_pairs_dijkstra_path(G)

# visualize graph
pos = nx.circular_layout(G)  # Circular layout
labels = {node: node for node in G.nodes()}  # Node labels
edge_labels = nx.get_edge_attributes(G, 'weight')  # Edge labels

plt.figure(figsize=(8, 6))  # Set figure size
nx.draw_networkx(G, pos, with_labels=False, node_color='lightblue', node_size=500, alpha=0.8)
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# print forwarding tables
for node, table in forwarding_tables:
    print("\n Forwarding table for node", node)
    for destination, path in table.items():
        if destination != node:
            next_hop = path[1]
            link_weight = G[path[0]][next_hop]['weight']  # Fixed: Access weight from the correct edge
            print("Destination:", destination, "Next Hop:", next_hop, "Link Weight:", link_weight)


forwarding_tables = {}
for node in G.nodes:
    dist, prev, first_links = dijkstra(G, node)
    forwarding_tables[node] = first_links

print('\n 3)  Dijkstra’s Algorithm \n')

for node in forwarding_tables:
    print(f"Forwarding table for node {node}:")
    for dest, first_link in forwarding_tables[node].items():
        link = first_link
        if(first_link==None):
            continue
        print(f"Destination: {dest}, Link: {link}")
    print()

plt.title('Computer Network Graph')  # Add a title

plt.show()



