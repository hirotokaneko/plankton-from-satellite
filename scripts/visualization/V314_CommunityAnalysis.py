import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import networkx as nx
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]

#----------------------
# Function for plotting pie chart
#----------------------

def PlotTaxonomicBreakdown(ax, nodes, community_name):
	#Get the taxonomy of nodes
	DFtx = DFtaxo.loc[nodes,:]
	#Count "taxogroup1"
	taxa_counts = [sum(DFtx["taxogroup1"]==taxa) for taxa in taxo_index[:-1]]
	taxa_counts.append(sum(DFtx["taxogroup1"]!=DFtx["taxogroup1"]))
	taxa_counts = np.array(taxa_counts)
	#Count "taxogroup2"
	taxa_counts_2 = []
	for i in range(len(taxo_index)-1):
		cnt2 = [sum(DFtx["taxogroup2"]==taxa) for taxa in taxo_index_2[i]]
		taxa_counts_2 += cnt2
	taxa_counts_2.append(sum(DFtx["taxogroup2"]!=DFtx["taxogroup2"]))
	taxa_counts_2 = np.array(taxa_counts_2)
	#Set the size of pie
	size = 0.2
	distance = 0.7
	#Make a pie chart by "taxogroup2" (ordered by "taxogroup1") with count annotations
	nz_ind_2 = np.nonzero(taxa_counts_2)
	_, _, autotexts = ax.pie(taxa_counts_2[nz_ind_2], radius=distance-size, colors=np.array(taxo_colors_2)[nz_ind_2],
							 labels=np.array(sum(taxo_index_2, []))[nz_ind_2], labeldistance=1.1, pctdistance=distance, autopct="", startangle=90,
							 rotatelabels=True, textprops={"size":15}, wedgeprops=dict(width=size, edgecolor='w'))
	for i, a in enumerate(autotexts):
		a.set_text("{}".format(taxa_counts_2[nz_ind_2][i]))
	#Save to a PNG file
	ax.axis('equal')
	ax.set_title("Module {} (n={})".format(community_name, DFtx.shape[0]), fontsize=24, pad=100)

#----------------------

#----------------------
# Read data
#----------------------

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the list of network edges
DFedges = pd.read_csv("../data/{}/network.{}.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", header=None)
DFedges.columns = ["nodeA", "nodeB", "correlation"]

#Read the table of community membership
DFcom = pd.read_csv("../data/{}/community.{}.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", index_col=0)

#Read the list of ASV taxonomies
DFtaxo = pd.read_csv("../data/{}/eukbank_18SV4_asv.taxo.extracted".format(subdirec), delimiter="\t", index_col=0)

#----------------------

#Loop by community detection methods
list_com_detec_met = ["fast_greedy","infomap","label_prop","leading_eigen",
		      "leiden","louvain","spinglass","walktrap"] 
for com_detec_met in list_com_detec_met:

	#Get the number of communities
	print(com_detec_met)
	com_col_name = "mem_{}".format(com_detec_met)
	n_com = DFcom["mem_{}".format(com_detec_met)].max()
	list_coms = [int(i) for i in range(1,n_com+1)]

	#----------------------
    # Plot taxonomic breakdown of the full network
    #----------------------

	#Get index of "taxogroup1"
	taxo_index = list(DFtaxo["taxogroup1"].value_counts().index) + ["unclassified"]
	#Get index of "taxogroup2"
	taxo_index_2 = []
	for tx1 in taxo_index[:-1]:
		tx2_index = list(DFtaxo[DFtaxo["taxogroup1"]==tx1]["taxogroup2"].value_counts().index)
		taxo_index_2.append(tx2_index)
	taxo_index_2.append(["unclassified"])
	#Set colors for "taxogroup2"
	cmap = plt.get_cmap("tab20b")
	taxo_colors_2 = []
	for i, tx2s in enumerate(taxo_index_2):
		base_ind = (i%5)*4
		sub_cols_ind  = [base_ind+1,base_ind+2,base_ind+3]
		taxo_cols_2 = list(cmap(sub_cols_ind*(len(tx2s)//3) + sub_cols_ind[:(len(tx2s)%3)]))
		taxo_colors_2 += taxo_cols_2
	#Plot pie chart
	fig, ax = plt.subplots(figsize=(7,7))
	PlotTaxonomicBreakdown(ax=ax, nodes=DFcom.index, community_name="_")
	fig.tight_layout()
	fig.savefig("../figures/{}/V314.taxonomy.breakdown.{}.png".format(subdirec,NRM), format="png")
	plt.close(fig)

	#----------------------


	#Get positive weighted edges
	DFedges_pos = DFedges[DFedges["correlation"]>0]
	list_edges = [(DFedges_pos.loc[i,"nodeA"], DFedges_pos.loc[i,"nodeB"], {"weight":DFedges_pos.loc[i,"correlation"]}) for i in DFedges_pos.index]
	
	#Make a graph instance
	Go = nx.Graph()
	#Add edges to the graph
	Go.add_edges_from(list_edges)
	#Get the largest connected component
	Gcc = sorted(nx.connected_components(Go), key=len, reverse=True)
	G = Go.subgraph(Gcc[0])

	#----------------------
    # Plot sub-graph of each modules
    #----------------------

	print("Plot sub-graph and taxonomic breakdown of each modules...")
	for community in list_coms:
		print("community {}".format(community))

		#Get a list of node in the community
		list_nodes_in_com = list(DFcom.index[DFcom[com_col_name]==community])
		#Get the color of the community
		com_color = cm.jet(community/float(n_com))

		#Highlight edges and nodes of the commmunity
		list_G_node_size = [15 if node in list_nodes_in_com else 0 for node in G.nodes()]
		list_G_edge_colors = [com_color if (edge[0] in list_nodes_in_com)&(edge[1] in list_nodes_in_com) else "gray" for edge in G.edges()]
		list_G_edge_width = [0.5 if (edge[0] in list_nodes_in_com)&(edge[1] in list_nodes_in_com) else 0.2 for edge in G.edges()]
		
		#Visualize the graph
		np.random.seed(123)
		fig, ax = plt.subplots()
		pos = nx.spring_layout(G)
		nx.draw_networkx_nodes(G, pos, node_color=[com_color]*len(G.nodes()), edgecolors="black", linewidths=0.1, node_size=list_G_node_size)
		nx.draw_networkx_edges(G, pos, edge_color=list_G_edge_colors, width=list_G_edge_width)
		ax.axis("off")
		fig.savefig("../figures/{}/community/V314.subnetwork.{}.{}.community{}.png".format(subdirec,NRM,com_detec_met,community), format="png")
		plt.close(fig)

		#Plot pie chart of the community's taxonomic breakdown
		fig, ax = plt.subplots(figsize=(7,5))
		PlotTaxonomicBreakdown(ax=ax, nodes=list_nodes_in_com, community_name=community)
		fig.tight_layout()
		fig.savefig("../figures/{}/community/V314.taxonomy.breakdown.{}.{}.community{}.png".format(subdirec,NRM,com_detec_met,community), format="png")
		plt.close(fig)

		#Save the taxonomy table of the community
		DFtaxo_com = DFtaxo.loc[list_nodes_in_com,:]
		DFtaxo_com.to_csv("../data/{}/V314.taxonomy.breakdown.{}.{}.community{}.tsv".format(subdirec,NRM,com_detec_met,community), sep="\t")

	#----------------------

	#----------------------
	# Plot summary figure of taxonomic breakdown of modules
	#----------------------

	#Make subplots
	fig, axes = plt.subplots(2, 3, figsize=(20,15))

	print("Plot taxonomic breakdown of each modules...")
	for i, community in enumerate(list_coms):
		print("community {}".format(community))

		#Get a list of node in the community
		list_nodes_in_com = list(DFcom.index[DFcom[com_col_name]==community])

		if i < 6:
			#Set subplot
			ax = axes[i//3,i%3]
			#Plot pie chart of the community's taxonomic breakdown
			PlotTaxonomicBreakdown(ax=ax, nodes=list_nodes_in_com, community_name=community)

	fig.tight_layout()
	fig.savefig("../figures/{}/community/V314.taxonomy.breakdown.{}.{}.summary.png".format(subdirec,NRM,com_detec_met), format="png")
	plt.close(fig)

	#----------------------
