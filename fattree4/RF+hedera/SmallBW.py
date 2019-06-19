
import sys
def small_flow_bw(flows, paths, graph):
	
	if not flows:
		return graph
	for flow in flows:
		datapaths = paths.get(flow['src']).get(flow['dst'])
		if len(datapaths) == 1:
			flow['path'] = datapaths[0]
		else:
			flow['path'] = datapaths[flow['src'] % 2]

	
	change_flow = True
	while(change_flow and flows):
		graph, change_flow, flows = rest_bw(flows, graph)
	# new_flows = rest_bw(flows, graph)
	return graph

def rest_bw(flows, graph):
	M = {} 
	for flow in flows:
		if len(flow['path']) == 3:
			M.setdefault(flow['path'][0], {})
			M.setdefault(flow['path'][1], {})
			M[flow['path'][0]].setdefault(flow['path'][1], 0)
			M[flow['path'][1]].setdefault(flow['path'][2], 0)
		else:
			M.setdefault(flow['path'][0], {})
			M.setdefault(flow['path'][1], {})
			M.setdefault(flow['path'][2], {})
			M.setdefault(flow['path'][3], {})
			M[flow['path'][0]].setdefault(flow['path'][1], 0)
			M[flow['path'][1]].setdefault(flow['path'][2], 0)
			M[flow['path'][2]].setdefault(flow['path'][3], 0)
			M[flow['path'][3]].setdefault(flow['path'][4], 0)

	for flow in flows:
		if len(flow['path']) == 3:
			M[flow['path'][0]][flow['path'][1]] += 1
			M[flow['path'][1]][flow['path'][2]] += 1
		else:
			M[flow['path'][0]][flow['path'][1]] += 1
			M[flow['path'][1]][flow['path'][2]] += 1
			M[flow['path'][2]][flow['path'][3]] += 1
			M[flow['path'][3]][flow['path'][4]] += 1
	# for m in M:
	# 	print m, M[m]
	if not M:
		return graph, False, flows

	return reduce_bw(M, flows, graph)

def reduce_bw(M, flows, graph):
	change_flow = False
	flowList = []
	tmp_graph = graph.copy()
	
	for edge in tmp_graph.edges(data=True):
		value = M.get(edge[0], 1)
		if value == 1:
			edge[2]['weight'] = float(graph.get_edge_data(edge[0], edge[1])['weight'])
		else:
			edge[2]['weight'] = float(graph.get_edge_data(edge[0], edge[1])['weight']) / float(value.get(edge[1], 1))

	for flow in flows:
		path = flow['path']
		if len(path) < 3:
			continue
		elif len(path) == 3:
			for edge in tmp_graph.edges(data = True):
				if edge[0] == path[0] and edge[1] == path[1] and edge[2]['weight'] < flow['demand']:
					flow['demand'] = edge[2]['weight']
				elif edge[0] == path[1] and edge[1] == path[2] and edge[2]['weight'] < flow['demand']:
					flow['demand'] = edge[2]['weight']
		else:
			for edge in tmp_graph.edges(data = True):
				if edge[0] == path[0] and edge[1] == path[1] and edge[2]['weight'] < flow['demand']:
					flow['demand'] = edge[2]['weight']
				elif edge[0] == path[1] and edge[1] == path[2] and edge[2]['weight'] < flow['demand']:
					flow['demand'] = edge[2]['weight']
				elif edge[0] == path[2] and edge[1] == path[3] and edge[2]['weight'] < flow['demand']:
					flow['demand'] = edge[2]['weight']
				elif edge[0] == path[3] and edge[1] == path[4] and edge[2]['weight'] < flow['demand']:
					flow['demand'] = edge[2]['weight']

	
	for flow in flows:
		# print flow
		if flow['demand'] > (float(flow['size']) / 100000.0):
			flow['demand'] = float(flow['size']) / 100000.0
			flowList.append(flow)
			flows.remove(flow)
			change_flow = True

	
	if change_flow:
		new_graph = compute_graph(graph, flowList)
	else:
		new_graph = compute_graph(graph, flows)

	return new_graph, change_flow, flows
	# return flows

def compute_graph(graph, flows):
	for flow in flows:
		path = flow['path']
		if len(path) < 3:
			continue
		elif len(path) == 3:
			for edge in graph.edges(data = True):
				if edge[0] == path[0] and edge[1] == path[1]:
					edge[2]['weight'] -= flow['demand']
				elif edge[0] == path[1] and edge[1] == path[2]:
					edge[2]['weight'] -= flow['demand']
		else:
			for edge in graph.edges(data = True):
				if edge[0] == path[0] and edge[1] == path[1]:
					edge[2]['weight'] -= flow['demand']
				elif edge[0] == path[1] and edge[1] == path[2]:
					edge[2]['weight'] -= flow['demand']
				elif edge[0] == path[2] and edge[1] == path[3]:
					edge[2]['weight'] -= flow['demand']
				elif edge[0] == path[3] and edge[1] == path[4]:
					edge[2]['weight'] -= flow['demand']
	return graph