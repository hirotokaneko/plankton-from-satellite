import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import sys

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

#Read the grid data
DFg = pd.read_csv("../input/eukbank_satellite_grid.elev.prov.tsv", delimiter="\t", index_col=0)

#Read the clr-sigmoid transformed frequency table
DFs = pd.read_csv("../data/{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.fz_nz.sigmoid.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM), delimiter="\t", index_col=0)
#Add a column of latitude to the frequency table
DFs["GridLat"] = DFg.loc[DFs.index, "GridLat"]
#Sort the frequency table by latitude
DFs_sort = DFs.sort_values(by="GridLat", ascending=False)

#Plot the monochrome heatmap of the clr-sigmoid transformed frequency table
fig, ax = plt.subplots(figsize=(12,10))
sns.heatmap(DFs_sort.iloc[:,:-1], cmap="binary", ax=ax)
fig.tight_layout()
fig.savefig("../figures/{}/V315.sigmoid.heatmap.png".format(subdirec), format="png")
fig.clf()

#List of used methods for community detection
list_com_detec_met = ["fast_greedy","infomap","label_prop","leading_eigen",
		      "leiden","louvain","spinglass","walktrap"] 
for com_detec_met in list_com_detec_met:

	print("Method ->", com_detec_met)
	#Read the table of edge satisfaction index and representative community
	DFesf = pd.read_csv("../data/{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,com_detec_met), delimiter="\t", index_col=0)
	#Add a column of latitude to the table of edge satisfaction
	DFesf["GridLat"] = DFg.loc[DFesf.index, "GridLat"]
	#Sort the edge satisfaction table by latitude
	DFesf_sort = DFesf.sort_values(by="GridLat", ascending=False)
	
	#Get the number of communities
	n_com = max(DFesf_sort["class"])
	#Get the matrix of edge satisfaction index values
	DFesf_sort_core = DFesf_sort.iloc[:,:-2]

	#Get the color of communities
	SRcol_color_pro = pd.Series(DFesf_sort_core.columns.astype(int), index=DFesf_sort_core.columns)
	SRcol_color = SRcol_color_pro.apply(lambda c: cm.jet(c/float(n_com)))
	#Get the list of representative communities in color
	SRrow_color = DFesf_sort["class"].apply(lambda c: cm.jet(c/float(n_com)))

	#Plot the monochrome heatmap of the matrix of edge satisfaction with an annotation of representative community
	plt.rcParams["font.size"] = 16
	g = sns.clustermap(DFesf_sort_core, col_cluster=False, row_cluster=False, row_colors=SRrow_color,
					   col_colors=SRcol_color, cmap="binary", xticklabels=0, yticklabels=0)
	g.savefig("../figures/{}/V315.edge.satisfaction.heatmap.{}.{}.png".format(subdirec,NRM,com_detec_met), format="png")

