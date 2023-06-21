import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import networkx as nx
import sys
import itertools

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the list of network edges
DFedges = pd.read_csv("../data/{}/network.{}.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", header=None)
DFedges.columns = ["nodeA", "nodeB", "correlation"]
#Read the table of community membership
DFcom = pd.read_csv("../data/{}/community.{}.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", index_col=0)

#Plot a histgram of edge weights (= correation coefficient)
fig, ax = plt.subplots()
sns.histplot(DFedges["correlation"], ax=ax)
fig.savefig("../figures/{}/V313.correlation.histgram.{}.png".format(subdirec,NRM), format="png")
plt.close(fig)

#Get positive weighted edges
DFedges_pos = DFedges[DFedges["correlation"]>0]
#Make a list of positive weighted edges in "networkx" format
list_edges = [(DFedges_pos.loc[i,"nodeA"], DFedges_pos.loc[i,"nodeB"], {"weight":DFedges_pos.loc[i,"correlation"]}) for i in DFedges_pos.index]

#Make a graph instance
Go = nx.Graph()
#Add edges to the graph
Go.add_edges_from(list_edges)
#Get the largest connected component
Gcc = sorted(nx.connected_components(Go), key=len, reverse=True)
G = Go.subgraph(Gcc[0])

#Plot a histgram of node degrees (considering only positive edges)
fig, ax = plt.subplots()
list_G_degrees = [G.degree(weight="weight")[node] for node in G.nodes()]
sns.histplot(x=list_G_degrees, ax=ax)
fig.savefig("../figures/{}/V313.degree.histgram.{}.png".format(subdirec,NRM), format="png")
plt.close(fig)

#List of used methods for community detection
list_com_detec_met = ["fast_greedy","infomap","label_prop","leading_eigen",
					  "leiden","louvain","spinglass","walktrap"]

for com_detec_met in list_com_detec_met:
	
	#Get the number of communities
	com_col_name = "mem_{}".format(com_detec_met)	
	n_com = DFcom["mem_{}".format(com_detec_met)].max()
	
	#Visualize the graph---------------------
	np.random.seed(123)
	fig, ax = plt.subplots(figsize=(6,4.5))
	pos = nx.spring_layout(G, weight="weight")
	for community in range(1,n_com+1):
		nodes_in_com = list(DFcom.index[DFcom[com_col_name] == community])
		nx.draw_networkx_nodes(G, pos, nodelist=nodes_in_com,
				       node_color=[cm.jet(community/float(n_com))]*len(nodes_in_com), 
					   edgecolors="black", linewidths=0.1, node_size=15, label=community)
	nx.draw_networkx_edges(G, pos, edge_color="gray", width=0.5)	
	ax.axis("off")
	leg = ax.legend(bbox_to_anchor=(0.95,1), loc='upper left', scatterpoints=1, fontsize=16)
	leg.set_title("Module", prop={'size': 14, 'weight': 'heavy'})
	fig.tight_layout()
	fig.savefig("../figures/{}/V313.network.{}.{}.png".format(subdirec,NRM,com_detec_met), format="png")
	plt.close(fig)
	#-----------------------------------------

	#Plot the size of communities-------------
	fig, ax = plt.subplots(figsize=(7,5))
	SRcom_mem_counts = DFcom[com_col_name].value_counts()
	ax.bar(np.arange(n_com), SRcom_mem_counts.values)
	ax.set_xticks(np.arange(n_com))
	ax.set_xticklabels(list(SRcom_mem_counts.index))
	ax.set_xlabel("Module", fontsize=16)
	ax.set_ylabel("#Nodes", fontsize=16)
	ax.tick_params(labelsize =14)
	figure_path = "../figures/{}/V313.community.breakdown.{}.{}.png".format(subdirec,NRM,com_detec_met)
	fig.savefig(figure_path, format="png")
	plt.close(fig)
	#-----------------------------------------

	#Plot the connection among communities----
	
	#Calculate the weighted sum of edges connecting two communites
	list_coms = [i for i in range(1,n_com+1)]
	DFinter = pd.DataFrame(0, index=list_coms, columns=list_coms)
	for i in DFedges_pos.index:
		nodeA, nodeB = DFedges_pos.loc[i,"nodeA"], DFedges_pos.loc[i,"nodeB"]
		if (nodeA in DFcom.index)&(nodeB in DFcom.index):
			comA, comB = DFcom.loc[nodeA,com_col_name], DFcom.loc[nodeB,com_col_name]
			DFinter.loc[comA, comB] += DFedges_pos.loc[i,"correlation"]
	#Make a list of connection strengths in "networkx" format
	list_inter_edges = [(i, j, {"weight":DFinter.loc[i,j]}) for i, j in itertools.combinations(list_coms,2)]
	#Make a graph instance
	Ginter = nx.Graph()
	#Add edges to the graph
	Ginter.add_edges_from(list_inter_edges)

	#Visualize the graph of community connections
	fig, ax = plt.subplots()
	pos = nx.circular_layout(Ginter)
	for community in list_coms:
		nx.draw_networkx_nodes(Ginter, pos, nodelist=[community],
							   node_color=[cm.jet(community/float(n_com))],
							   edgecolors="black", linewidths=0.1, node_size=200, label=community)
	all_weights = [data['weight'] for (node1,node2,data) in Ginter.edges(data=True)]
	unique_weights = list(set(all_weights))
	for weight in unique_weights:
		weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in Ginter.edges(data=True) if edge_attr['weight']==weight]
		nx.draw_networkx_edges(Ginter,pos,edgelist=weighted_edges,width=weight*2,edge_color="grey")
	ax.axis("off")
	ax.axis('equal')
	figure_path = "../figures/{}/V313.community.link.{}.{}.png".format(subdirec,NRM,com_detec_met)
	fig.savefig(figure_path, format="png")
	plt.close(fig)

	#-----------------------------------------
