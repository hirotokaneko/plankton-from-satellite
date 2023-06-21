import pandas as pd
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

#List of used methods for community detection
list_com_detec_met = ["fast_greedy","infomap","label_prop","leading_eigen",
					  "leiden","louvain","spinglass","walktrap"] 
for com_detec_met in list_com_detec_met:

	print("Method ->", com_detec_met)
	#Read the table of edge satisfaction index and representative community
	DFesf = pd.read_csv("../data/{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,com_detec_met), delimiter="\t", index_col=0)
	#Get the number of communities
	n_com = max(DFesf["class"])

	listDFsps = []
	listDFtxs = []
	for com in range(1,n_com+1):
		#Read the taxonomy table of the community
		DFtx = pd.read_csv("../data/{}/V314.taxonomy.breakdown.{}.{}.community{}.tsv".format(subdirec,NRM,com_detec_met,com), delimiter="\t", index_col=0)
		#Count lineages of the community
		DFsp = pd.DataFrame(DFtx["taxonomy"].value_counts())
		#列名を変える
		DFsp = DFsp.rename(columns={"taxonomy": "community {}".format(com)})
		#カウントデータフレームをリストに追加
		listDFsps.append(DFsp)
		#Add community to the taxonomy table 
		DFtx["community"] = com
		listDFtxs.append(DFtx)

	#Concatenate lineage counts tables
	DFspcat = pd.concat(listDFsps, axis=1)
	#Replace NaN with 0
	DFspcat = DFspcat.fillna(0)
	DFspcat = DFspcat.astype(int)
	#Save the lineage counts table
	DFspcat = DFspcat.sort_index()
	DFspcat.to_csv("../data/{}/V319.species.breakdown.{}.{}.tsv".format(subdirec,NRM,com_detec_met), sep="\t")

	#Concatenate taxonomy tables
	DFtxcat = pd.concat(listDFtxs, axis=0)
	#Save the taxonomy table with community annotation
	DFtxcat.to_csv("../data/{}/V319.taxonomy.breakdown.{}.{}.tsv".format(subdirec,NRM,com_detec_met), sep="\t")
