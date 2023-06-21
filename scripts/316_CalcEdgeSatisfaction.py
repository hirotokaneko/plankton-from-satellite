import pandas as pd
import numpy as np
import networkx as nx
from scipy.special import expit
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]

print("Loading data")
#Load the table of detcted communities
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)
DFcom = pd.read_csv("{}/community.{}.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", index_col=0)

#Load the frequency table
DFf = pd.read_csv("{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.fz_nz.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), delimiter="\t", index_col=0)
print(DFf.shape)
DFf.head()

#Sigmoid trasformation
DFf2 = DFf.copy()
DFf2[DFf2==0.0] = np.nan #Replace 0 with nan
DFf2_sig = expit(DFf2) #Sigmoid transformation
DFf_sig = DFf2_sig.fillna(0.0) #Place 0 back
#Save the sigmoid trasformed frequency table
DFf_sig.to_csv("{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.fz_nz.sigmoid.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), sep="\t")

#Load FlashWeave edges
DFedges = pd.read_csv("{}/network.{}.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", header=None)
DFedges.columns = ["nodeA", "nodeB", "correlation"]

#Create network with positive edges
DFedges_pos = DFedges[DFedges["correlation"]>0] #Keep positive edges
list_edges = [(DFedges_pos.loc[i,"nodeA"], DFedges_pos.loc[i,"nodeB"], {"weight":DFedges_pos.loc[i,"correlation"]}) for i in DFedges_pos.index] #Make a list of edge tuples
G = nx.Graph() #Make empty graph
G.add_edges_from(list_edges) #Add edges from the list

#Define a function for calculating the sum of edges' presence
def CalcSumEdgesPresence(Graph, sample):
	sum_edges_presence = 0.0
	for edge in Graph.edges(data = True):
		#Sigmoid frequency of two nodes
		sig_nodeA = DFf_sig.loc[sample,edge[0]]
		sig_nodeB = DFf_sig.loc[sample,edge[1]]
		#Smaller frequency
		min_sig = min(sig_nodeA,sig_nodeB)
		#Edge weight
		weight = edge[2]["weight"]
		#Calculate edge's presence as frequency*edge weight
		edge_presence = min_sig*weight
		#Add the presence of this edge
		sum_edges_presence += edge_presence
	return sum_edges_presence

print("Calculate edge satisfaction...")
#List of community detecion methods
list_com_detec_met = ["fast_greedy","infomap","label_prop","leiden",
		      "louvain","spinglass","walktrap", "leading_eigen"] 
for com_detec_met in list_com_detec_met:

	#Community detection method of given data
	print("Method ->", com_detec_met)
	com_col_name = "mem_{}".format(com_detec_met)
	n_com = DFcom[com_col_name].max()
	list_com = [i for i in range(1,n_com+1)]
	
	#Calculate edge satisfaction for each community
	DFesf = pd.DataFrame(index=DFf.index)
	for community in list_com:
		print("community", community)

		#List of nodes in community
		list_nodes_in_com = list(DFcom.index[DFcom[com_col_name]==community])
		#Make community subgraph
		Gcom = G.subgraph(list_nodes_in_com)
		#Sum of edge wights
		sum_edges_com = sum([i[2]["weight"] for i in Gcom.edges(data = True)])

		#List of the sum of edges' presence of each sample
		list_sep_com = []
		for sample in DFf_sig.index:
			sep_com = CalcSumEdgesPresence(Gcom, sample)
			list_sep_com.append(sep_com)
	
		#Calculate edge satisfaction index for each sample
		esf_values = np.array(list_sep_com)/sum_edges_com
		#Add satisfaction index to a dictionary 
		DFesf[community] = esf_values

	#Assign representative class for each sample
	DFesf["class"] = DFesf.apply(lambda x: DFesf.columns[np.argmax(x)], axis=1)

	#Save the table of edge satisfaction index and class
	DFesf.to_csv("{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,com_detec_met), sep="\t")

