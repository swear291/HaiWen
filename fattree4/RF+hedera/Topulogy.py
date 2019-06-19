#!-*- coding:utf8-*-
 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import sys
from Flow import *
from Get_Model import *
from DemandEst import *
from tool import *
from SmallBW import *

#构建fattree，每条边权重为1
G = nx.DiGraph()

G.add_weighted_edges_from([(1001, 2001, 1), (1001, 2003, 1), (1001, 2005, 1), (1001, 2007, 1)])
G.add_weighted_edges_from([(1002, 2001, 1), (1002, 2003, 1), (1002, 2005, 1), (1002, 2007, 1)])
G.add_weighted_edges_from([(1003, 2002, 1), (1002, 2004, 1), (1002, 2006, 1), (1002, 2008, 1)])
G.add_weighted_edges_from([(1004, 2002, 1), (1002, 2004, 1), (1002, 2006, 1), (1002, 2008, 1)])

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

#==================================================================
hostList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
#根据fattree找到端口到端口之间的所有最短路径
_graph = G.copy()
k = 5
paths = {}
for src in hostList:
	paths.setdefault(src, {src: []})
	for dst in hostList:
		if src == dst:
			continue
		paths[src].setdefault(dst, {dst: 1})
		paths[src][dst] = k_shortest_paths(_graph, src, dst, weight='weight', k=6)



#==================================================================
bigFlowList = [] #没有传输过的大流
smallFlowList = [] #没有传输过的小流
bigTraffic = [] #处于传输过程中的大流
smallTraffic = [] #处于传输过程中的小流
bw_utili = {} #存储各时间点的带宽利用率

df_big = pd.DataFrame()
df_small = pd.DataFrame()
df_big, df_small = get_df() #通过RF模型得出预测流信息
# print df_small
# sys.exit()
for index, row in df_big.iterrows():
    bigFlowList.append({'src': int(row['src']), 'dst': int(row['dst']), 'demand': 0,
				'converged':False, 'receiver_limited': False, 'size': int(row['y_size']), 
				'time': int(row['time']), 'conf': row['Confidence']})
for index, row in df_small.iterrows():
    smallFlowList.append({'src': int(row['src']), 'dst': int(row['dst']), 'demand': 1.0,
				'converged':False, 'receiver_limited': False, 'size': int(row['y_size']), 
				'time': int(row['time']), 'path': [], 'conf': row['Confidence']})

total_bw = 32
time_slot_data = 100

big_count = len(bigFlowList)
big_finish = 0
all_time = 0
all_flow = len(bigFlowList) + len(smallFlowList)

for i in xrange(2500):
	# print '=========================================================='
	used_bw = 0 #记录实际使用带宽
	_graph = G.copy()
	for flow in bigTraffic: #每个time slot检查传输完成的流并从数组中剔除
		flow['size'] -= time_slot_data * 1000 * flow['demand']
		if flow['size'] <= 0:
			big_finish += 1
			bigTraffic.remove(flow)
		all_time += 1
			
	for flow in smallTraffic:
		flow['size'] -= time_slot_data * 1000 * flow['demand']
		if flow['size'] <= 0:
			smallTraffic.remove(flow)
		all_time += 1

	# for flow in smallFlowList:
	# 	print flow

	for flow in smallFlowList: #将开始时间满足当前time slot的流加入数组
		if flow['time'] > 100 * i and flow['time'] <= 100 * (i + 1):
			smallTraffic.append(flow)
			smallFlowList.remove(flow)
			all_time += 1

	# small_graph = G.copy()
	# small_flows = small_flow_bw(smallTraffic, paths, small_graph)

	real_graph = small_flow_bw(smallTraffic, paths, _graph)

	# sys.exit()

	for flow in bigFlowList:
		if flow['time'] > 100 * i and flow['time'] <= 100 * (i + 1):
			bigTraffic.append(flow)
			bigFlowList.remove(flow)
			all_time += 1

	bigTraffic = demand_estimation(bigTraffic, hostList) #对预测出的大流进行需求评估

	for flow in bigTraffic: #对demand的流进行链路分配
		global_first_fit(flow, paths, real_graph)

	for edge in real_graph.edges(data=True): #记录当前fattree中的剩余带宽
		used_bw += edge[2]['weight']

	bw_utili[i] = 1 - (used_bw / total_bw)
	# print used_bw

utili_list = []
tmp = 0
for utili in bw_utili:
	utili_list.append(bw_utili[utili])

for ele in utili_list:
	if ele == tmp:
		utili_list.remove(ele)
	else:
		tmp = ele

print('big flow finish:' + str(float(big_finish) / float(big_count)))
print('average flow finish time:' + str(float(all_time) / float(all_flow)))

plot_df = pd.DataFrame()
plot_df['utili'] = utili_list

plt.plot(plot_df['utili'])
plt.show()



# for path in paths:
# 	print str(paths[path])

# nx.draw(G)
# plt.savefig("youxiangtu.png")
# plt.show()