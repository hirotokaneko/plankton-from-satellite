import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
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

#Read the satellite data
DFs = pd.read_csv("../input/eukbank_imputed_satellite_data.tsv", delimiter="\t", index_col=0, dtype="object").astype(float)

#Loop by community detection methods
list_com_detec_met = ["fast_greedy","leading_eigen","leiden","louvain","spinglass"]
for com_detec_met in list_com_detec_met:
	print(com_detec_met)

	#Read the table of edge satisfaction index and representative community
	DFesf = pd.read_csv("../data/{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,com_detec_met), delimiter="\t", index_col=0)
	#Get the number of communities
	n_com = max(DFesf["class"])

	#Make a table of representative community and temperature
	DFcat = pd.concat([DFesf["class"], DFs["SST"]], join="inner", axis=1)

	#Plot representative community vs. temperature
	fig, ax = plt.subplots(figsize=(7,5))
	for c in range(1,n_com+1):
		com_color = cm.jet(c/float(n_com))
		com_num = sum(DFcat["class"].values==c)
		ax.scatter(DFcat.loc[DFcat["class"].values==c,"SST"], [c]*com_num, color=com_color, label=c, s=20)
	ax.legend(bbox_to_anchor=(1.3,1))
	fig.tight_layout()
	fig.savefig("../figures/{}/V514.class.sst.{}.{}.png".format(subdirec,NRM,com_detec_met), format="png")
	plt.close(fig)

