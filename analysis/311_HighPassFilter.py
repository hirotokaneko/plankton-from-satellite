import pandas as pd
import numpy as np
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Load the frequency table
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
DFf = pd.read_csv("../input/asv.{}.filt.dd.grid.sat.{}{}tsv".format(SIZ,opo2,tpr2), delimiter="\t", index_col=0, dtype="object").astype(int)

#10% of sample number
data_size = int(np.round(DFf.shape[0]*0.1))
#<data_size>-th highest frequency of each ASVs
frq_cutoffs = np.array([DFf[asv].sort_values(ascending=False)[data_size-1] for asv in DFf.columns])
#Save <frq_cutoffs> to a text file
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)
with open("{}/asv.{}.filt.dd.grid.sat.{}{}bound.txt".format(subdirec,SIZ,opo2,tpr2), "w") as f:
	for i in frq_cutoffs:
		f.write("{}\n".format(i))

#Keep ASVs with <frq_cutoffs> >= given minimum
frq_filt = int(FRQ)
asv_through = DFf.columns[frq_cutoffs >= frq_filt]

#Save the frequency table of kept ASVs
DFff = DFf.loc[:,asv_through]
DFff.to_csv("{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), sep="\t")

