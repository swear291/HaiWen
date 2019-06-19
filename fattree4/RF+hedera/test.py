import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tool import *

G = nx.DiGraph()

G.add_weighted_edges_from([(1001, 2001, 1), (1001, 2003, 1), (1001, 2005, 1), (1001, 2007, 1)])
G.add_weighted_edges_from([(1002, 2001, 1), (1002, 2003, 1), (1002, 2005, 1), (1002, 2007, 1)])
G.add_weighted_edges_from([(1003, 2002, 1), (1003, 2004, 1), (1003, 2006, 1), (1003, 2008, 1)])
G.add_weighted_edges_from([(1004, 2002, 1), (1004, 2004, 1), (1004, 2006, 1), (1004, 2008, 1)])

G.add_weighted_edges_from([(2001, 1001, 1), (2001, 1002, 1), (2001, 3001, 1), (2001, 3002, 1)])
G.add_weighted_edges_from([(2002, 1003, 1), (2002, 1004, 1), (2002, 3001, 1), (2002, 3002, 1)])
G.add_weighted_edges_from([(2003, 3003, 1), (2003, 3004, 1), (2003, 1001, 1), (2003, 1002, 1)])
G.add_weighted_edges_from([(2004, 3003, 1), (2004, 3004, 1), (2004, 1003, 1), (2004, 1004, 1)])

G.add_weighted_edges_from([(2005, 1001, 1), (2005, 1002, 1), (2005, 3005, 1), (2005, 3006, 1)])
G.add_weighted_edges_from([(2006, 1003, 1), (2006, 1004, 1), (2006, 3005, 1), (2006, 3006, 1)])
G.add_weighted_edges_from([(2007, 3007, 1), (2007, 3008, 1), (2007, 1001, 1), (2007, 1002, 1)])
G.add_weighted_edges_from([(2008, 3007, 1), (2008, 3008, 1), (2008, 1003, 1), (2008, 1004, 1)])

G.add_weighted_edges_from([(3001, 2001, 1), (3001, 2002, 1), (3001, 1, 1), (3001, 2, 1)])
G.add_weighted_edges_from([(3002, 2001, 1), (3002, 2002, 1), (3002, 3, 1), (3002, 4, 1)])
G.add_weighted_edges_from([(3003, 2003, 1), (3003, 2004, 1), (3003, 5, 1), (3003, 6, 1)])
G.add_weighted_edges_from([(3004, 2003, 1), (3004, 2004, 1), (3004, 7, 1), (3004, 8, 1)])

G.add_weighted_edges_from([(3005, 2005, 1), (3005, 2006, 1), (3005, 9, 1), (3005, 10, 1)])
G.add_weighted_edges_from([(3006, 2005, 1), (3006, 2006, 1), (3006, 11, 1), (3006, 12, 1)])
G.add_weighted_edges_from([(3007, 2007, 1), (3007, 2008, 1), (3007, 13, 1), (3007, 14, 1)])
G.add_weighted_edges_from([(3008, 2007, 1), (3008, 2008, 1), (3008, 15, 1), (3008, 16, 1)])

G.add_weighted_edges_from([(1, 3001, 1), (2, 3001, 1), (3, 3002, 1), (4, 3002, 1), (5, 3003, 1), (6, 3003, 1), (7, 3004, 1), (8, 3004, 1)])
G.add_weighted_edges_from([(9, 3005, 1), (10, 3005, 1), (11, 3006, 1), (12, 3006, 1), (13, 3007, 1), (14, 3007, 1), (15, 3008, 1), (16, 3008, 1)])

# for (u,v,d) in G.edges(data=True):
# 	print u, v, d['weight']

hostList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
_graph = G.copy()
paths = {}
for src in hostList:
	paths.setdefault(src, {src: []})
	for dst in hostList:
		if src == dst:
			continue
		paths[src].setdefault(dst, [])
		paths[src][dst] = k_shortest_paths(_graph, src, dst, weight='weight', k=6)

# for path in paths:
# 	for a in paths.get(path):
# 		for b in paths.get(path).get(a):
# 			print b

df = pd.DataFrame(paths)
df.to_csv('graph_result.csv')

# datapaths = paths.get(1).get(8)
# for data in datapaths:
# 	print data, datapaths[data]

# for a in paths.get(1).get(8):
# 	if G.get_edge_data(a[1], a[2])['weight'] < 2:
# 		print G.get_edge_data(a[1], a[2])


	# G[a[1]][a[2]]['weight'] = 2
	# c = G.get_edge_data(a[2], a[1])

		# print paths.get(path).get(a)

# print(len(G.edges(data=True)))
# G.get_edge_data(1, 2001)['weight'] = 0.2
# if G.get_edge_data(1, 2001)['weight'] >= 0.1:
# print G.get_edge_data(1, 2001)['weight']
# for a in G.edges(data=True):
# 	print a

# for a in G.edges(data=True):
# 	print a
# 	print a[2]['weight']
# nx.draw(G)
# plt.savefig("wuxiangtu.png")
# plt.show()

# G.add_weighted_edges_from([(3001, 2001, 1), (3001, 2002, 1)])
# G.add_weighted_edges_from([(3002, 2001, 1), (3002, 2002, 1)])

# G.add_weighted_edges_from([(3003, 2003, 1), (3003, 2004, 1)])
# G.add_weighted_edges_from([(3004, 2003, 1), (3004, 2004, 1)])

# G.add_weighted_edges_from([(3005, 2005, 1), (3005, 2006, 1)])
# G.add_weighted_edges_from([(3006, 2005, 1), (3006, 2006, 1)])

# G.add_weighted_edges_from([(3007, 2007, 1), (3007, 2008, 1)])
# G.add_weighted_edges_from([(3008, 2007, 1), (3008, 2008, 1)])

# G.add_weighted_edges_from([(2001, 1001, 1), (2001, 1002, 1), (2001, 3001, 1), (2001, 3002, 1)])
# G.add_weighted_edges_from([(2002, 1003, 1), (2002, 1004, 1), (2002, 3001, 1), (2002, 3002, 1)])

# G.add_weighted_edges_from([(2003, 1001, 1), (2003, 1002, 1), (2003, 3003, 1), (2003, 3004, 1)])
# G.add_weighted_edges_from([(2004, 1003, 1), (2004, 1004, 1), (2004, 3003, 1), (2004, 3004, 1)])

# G.add_weighted_edges_from([(2005, 1001, 1), (2005, 1002, 1), (2005, 3005, 1), (2005, 3006, 1)])
# G.add_weighted_edges_from([(2006, 1003, 1), (2006, 1004, 1), (2006, 3005, 1), (2006, 3006, 1)])

# G.add_weighted_edges_from([(2007, 1001, 1), (2007, 1002, 1), (2007, 3007, 1), (2007, 3008, 1)])
# G.add_weighted_edges_from([(2008, 1003, 1), (2008, 1004, 1), (2008, 3007, 1), (2008, 3008, 1)])

# G.add_weighted_edges_from([(1001, 2001, 1), (1001, 2003, 1), (1001, 2005, 1), (1001, 2007, 1)])
# G.add_weighted_edges_from([(1002, 2001, 1), (1002, 2003, 1), (1002, 2005, 1), (1002, 2007, 1)])
# G.add_weighted_edges_from([(1003, 2002, 1), (1003, 2004, 1), (1003, 2006, 1), (1003, 2008, 1)])
# G.add_weighted_edges_from([(1004, 2002, 1), (1004, 2004, 1), (1004, 2006, 1), (1004, 2008, 1)])


# def k_shortest_paths(graph, src, dst, weight='weight', k=5):
# 	"""
# 		Creat K shortest paths from src to dst.
# 		generator produces lists of simple paths, in order from shortest to longest.
# 	"""
# 	generator = nx.shortest_simple_paths(graph, source=src, target=dst, weight=weight)
# 	shortest_paths = {}
# 	try:
# 		for path in generator:
# 			if len(path) <= 5:
# 				shortest_paths[tuple(path)] = 1
# 		# print shortest_paths
# 		return shortest_paths
# 	except:
# 		self.logger.debug("No path between %s and %s" % (src, dst)) 

# def global_first_fit(flow):
# 	demand = flow['demand']
# 	datapaths = paths[flow['src']][flow['dst']]
# 	for key, value in datapaths.items():
# 		if value >= demand:
# 			flow['datapath'] = key
# 			traffic_load_sub(key, value)

# def traffic_load_sub(datapath, bw):
# 	for path in paths:
# 		for a in paths.get(path):
# 			for b in paths.get(path).get(a):
# 				if datapath[0] in path and datapath[1] in path or datapath[1] in path and datapath[2] in path or datapath[2] in path and datapath[3] in path or datapath[3] in path and datapath[4] in path or datapath[4] in path and datapath[5] in path:
# 					paths.get(path).get(a)[b] = paths.get(path).get(a).get(b) - bw