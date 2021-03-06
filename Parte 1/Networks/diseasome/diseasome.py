import matplotlib.pyplot as plt
import networkx as nx
import operator
import sys
import csv 

#load a graph using the name of the network in the current folder
def load_graph(network_name = "diseasome"):
	G = nx.Graph() 
	f = True
	with open('nodes_' + network_name + '.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			if(f == True):
				f = False
				continue 
			G.add_node(row[0])

	f = True
	with open('edges_' + network_name + '.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			if(f == True):
				f = False
				continue 
			G.add_edge(row[0], row[1])

	return G

#orders the nodes using the metric
def get_ordered_nodes(G):
	#For highest degree_centrality
	metric_dic = nx.degree_centrality(G)

	#For highest betweenes_centrality
	#metric_dic = nx.betweenness_centrality(G)
	sorted_nodes = sorted(metric_dic.items(), key=operator.itemgetter(1), reverse=True)
	return sorted_nodes


def algo2(G, iterations, print_skip_number=1, file_name="output"):
	## first sort by the metric in decending order
	## than remove one by one n times and for each time compute the
	## connected components
	print "skip: " + str(print_skip_number)
	sorted_nodes = get_ordered_nodes(G)
	with open(file_name + ".csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for i in range(0, iterations):
			print "Disconnecting %s" % (sorted_nodes[i][0]) 
			G.remove_node(sorted_nodes[i][0])
			ncci = nx.number_connected_components(G)
			if i % print_skip_number == 0:
				Gc = max(nx.connected_component_subgraphs(G), key=len)
				Gcn = nx.number_of_nodes(Gc)
				writer.writerow([str(i + 1), str(ncci), str(Gcn)])
				print "%d,%d,%d" % (i + 1, ncci, Gcn)
				

	return G


G = None
#print 'Network name: ' + sys.argv[1]
if len(sys.argv) > 0:
	G = load_graph(network_name=sys.argv[1])
else:
	G = load_graph()

ncc1 = nx.number_connected_components(G)
#print "Number of CC at start = %d" % (ncc1)
Gc = max(nx.connected_component_subgraphs(G), key=len)

if len(sys.argv) == 4:
	G = algo2(G, G.number_of_nodes() - 1, print_skip_number=int(sys.argv[2]))
elif len(sys.argv) == 5:
	G = algo2(G, G.number_of_nodes() - 1, print_skip_number=int(sys.argv[2]), file_name=sys.argv[3])
else:
	G = algo2(G, G.number_of_nodes() - 1)

nx.draw(G, pos=nx.spring_layout(G), node_size=5, node_color='orange')

plt.draw()
plt.show()
