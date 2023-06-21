import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
AAJ = sys.argv[5]
NRM = sys.argv[6]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Loop by satellite feature sets
feature_sets = ["space","product","rrs","satellite","allfeat"]
for fts in feature_sets:
	print(">>", fts)

	#Read the UMAP projections
	DFsc_emmb = pd.read_csv("../data/{}/umap/umap.random.{}.{}.tsv".format(subdirec, AAJ, fts), delimiter="\t", index_col=0)
	DFeuk_sc_emmb = pd.read_csv("../data/{}/umap/umap.eukbank.{}.{}.tsv".format(subdirec, AAJ, fts), delimiter="\t", index_col=0)
	X_sc_emmb = DFsc_emmb.values
	Xeuk_sc_emmb = DFeuk_sc_emmb.values

	#Loop by community detection methods
	list_com_detec_met = ["fast_greedy","leading_eigen","leiden","louvain","spinglass"] 
	for com_detec_met in list_com_detec_met:
		print(com_detec_met)

		#Read the table of edge satisfaction index and representative community
		DFesf = pd.read_csv("../data/{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,com_detec_met), delimiter="\t", index_col=0)
		#Get the number of communities
		n_com = max(DFesf["class"])

		#Plot representative communities on the UMAP projection
		fig, ax = plt.subplots(figsize=(9,5))
		ax.scatter(X_sc_emmb[:,0], X_sc_emmb[:,1], color="lightgrey", s=5)
		for c in range(1,n_com+1):
			com_color = cm.jet(c/float(n_com))
			ax.scatter(Xeuk_sc_emmb[DFesf["class"].values==c,0], Xeuk_sc_emmb[DFesf["class"].values==c,1], color=com_color, label=c, s=20, zorder=10)
		ax.set_xlabel("UMAP1", fontsize=16)
		ax.set_ylabel("UMAP2", fontsize=16)
		ax.tick_params(labelsize =14)
		leg = ax.legend(bbox_to_anchor=(1.3,1), fontsize=16)
		leg.set_title("Community\ntype", prop={"size": 14, "weight": "heavy"})
		fig.tight_layout()
		fig.savefig("../figures/{}/V513.class.umap.{}.{}.{}.{}.png".format(subdirec, AAJ, NRM, com_detec_met, fts), format="png")
		plt.close(fig)
