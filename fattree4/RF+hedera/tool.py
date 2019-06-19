import networkx as nx
import matplotlib.pyplot as plt
import sys


def k_shortest_paths(graph, src, dst, weight='weight', k=6):
	"""
		Creat K shortest paths from src to dst.
		generator produces lists of simple paths, in order from shortest to longest.
	"""
	generator = nx.shortest_simple_paths(graph, source=src, target=dst, weight=weight)
	shortest_paths = []
	try:
		for path in generator:
			if len(path) <= k:
				shortest_paths.append(path)
				print 'find one'
		# print shortest_paths
		return shortest_paths
	except:
		self.logger.debug("No path between %s and %s" % (src, dst)) 

def global_first_fit(flow, paths, _graph):
	demand = flow['demand']
	datapaths = paths.get(flow['src']).get(flow['dst'])
	# print demand
	maxpath = []
	bottleneck = 0
	for datapath in datapaths:
		if len(datapath) < 3:
			continue
	# 	if len(datapath) == 3:
	# 		if _graph.get_edge_data(datapath[0], datapath[1])['weight'] >= _graph.get_edge_data(datapath[1], datapath[2])['weight']:
	# 			if _graph.get_edge_data(datapath[1], datapath[2])['weight'] > bottleneck:
	# 				bottleneck = _graph.get_edge_data(datapath[1], datapath[2])['weight']
	# 				maxpath = datapath
	# 		else:
	# 			if _graph.get_edge_data(datapath[0], datapath[1])['weight'] > bottleneck:
	# 				bottleneck = _graph.get_edge_data(datapath[0], datapath[1])['weight']
	# 				maxpath = datapath
	# 	if len(datapath) == 5:
	# 		if _graph.get_edge_data(datapath[1], datapath[2])['weight'] >= _graph.get_edge_data(datapath[2], datapath[3])['weight']:
	# 			if _graph.get_edge_data(datapath[2], datapath[3])['weight'] > bottleneck:
	# 				bottleneck = _graph.get_edge_data(datapath[2], datapath[3])['weight']
	# 				maxpath = datapath
	# 		else:
	# 			if _graph.get_edge_data(datapath[1], datapath[2])['weight'] > bottleneck:
	# 				bottleneck = _graph.get_edge_data(datapath[1], datapath[2])['weight']
	# 				maxpath = datapath

	# if len(maxpath) == 3 and bottleneck >= demand:
	# 	_graph[maxpath[0]][maxpath[1]]['weight'] -= demand
	# 	_graph[maxpath[1]][maxpath[2]]['weight'] -= demand

	# if len(maxpath) == 5 and bottleneck >= demand:
	# 	_graph[maxpath[0]][maxpath[1]]['weight'] -= demand
	# 	_graph[maxpath[1]][maxpath[2]]['weight'] -= demand
	# 	_graph[maxpath[2]][maxpath[3]]['weight'] -= demand
	# 	_graph[maxpath[3]][maxpath[4]]['weight'] -= demand
		if len(datapath) == 3 and _graph.get_edge_data(datapath[0], datapath[1])['weight'] >= demand and _graph.get_edge_data(datapath[1], datapath[2])['weight'] >= demand:
			_graph[datapath[0]][datapath[1]]['weight'] -= demand
			_graph[datapath[1]][datapath[2]]['weight'] -= demand
			break

		if len(datapath) == 5 and _graph.get_edge_data(datapath[1], datapath[2])['weight'] >= demand and _graph.get_edge_data(datapath[2], datapath[3])['weight'] >= demand:
			flow['path'] = datapath
			_graph[datapath[0]][datapath[1]]['weight'] -= demand
			_graph[datapath[1]][datapath[2]]['weight'] -= demand
			_graph[datapath[2]][datapath[3]]['weight'] -= demand
			_graph[datapath[3]][datapath[4]]['weight'] -= demand
			break

