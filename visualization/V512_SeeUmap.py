import pandas as pd
import matplotlib.pyplot as plt
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
AAJ = sys.argv[5]

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

	#Visualize the UMAP projection
	fig, ax = plt.subplots(figsize=(7,5))
	ax.scatter(X_sc_emmb[:,0], X_sc_emmb[:,1], color="lightgray", s=5)
	ax.scatter(Xeuk_sc_emmb[:,0], Xeuk_sc_emmb[:,1], label="Eukbank", s=20, c="black", zorder=10)
	ax.set_xlabel("UMAP1", fontsize=16)
	ax.set_ylabel("UMAP2", fontsize=16)
	ax.tick_params(labelsize =14)
	fig.tight_layout()
	fig.savefig("../figures/{}/V512.umap.{}.{}.png".format(subdirec, AAJ, fts), format="png")
	plt.close(fig)
