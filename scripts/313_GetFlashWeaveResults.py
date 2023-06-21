import numpy as np
import pandas as pd
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Load index of frequency table
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
with open("flashweave/{}.{}{}samplename".format(SIZ,opo2,tpr2)) as f:
        samplename = [i.strip() for i in f]

#List of sacaling methods
list_test = ["fz","fz_nz","mi","mi_nz"]

for test_name in list_test:

	#Load the frequency table scaled by FlashWeave
	DFf = pd.read_csv("flashweave/{}.{}{}frq{}.{}.mat".format(SIZ,opo2,tpr2,FRQ,test_name), delimiter="\s+", header=None, dtype="object")

	#Load header of frequency table
	with open("flashweave/{}.{}{}frq{}.{}.header".format(SIZ,opo2,tpr2,FRQ,test_name)) as f:
		header = [i.strip().strip('\"') for i in f]

	#Set index and header of the scaled table
	DFf.index = samplename
	DFf.columns = header

	#Save the table
	subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)
	DFf.to_csv("{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,test_name), sep="\t")

