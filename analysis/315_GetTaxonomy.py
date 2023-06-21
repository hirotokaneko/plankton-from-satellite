import numpy as np
import pandas as pd
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Load the frequency table
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)
DFf = pd.read_csv("{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), delimiter="\t", index_col=0, dtype="object")

#Load the full taxonomy table
DFtaxo = pd.read_csv("../input/eukbank_18SV4_asv.taxo", delimiter="\t", index_col=0)

#Make a subset of taxonomy table
DFtaxo_f = DFtaxo.loc[DFf.columns,:]

#Save the table
DFtaxo_f.to_csv("{}/eukbank_18SV4_asv.taxo.extracted".format(subdirec), sep="\t")

