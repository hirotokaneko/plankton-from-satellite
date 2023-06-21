import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
ROW = sys.argv[5]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the boundary values of top 10% frequency
with open("../data/{}/asv.{}.filt.dd.grid.sat.{}{}bound.txt".format(subdirec,SIZ,opo2,tpr2), "r") as f:
    frq_cutoffs = np.array([int(i.strip()) for i in f])

#Get the maximum of boundary values
frq_cutoffs_max = max(frq_cutoffs)
#Get array up to the max. boundary value
x_arr = np.arange(frq_cutoffs_max+1)

#Calculate how many number of ASVs are kept when the cutoff for boundary value is given
if ROW == "write":
    with open("../data/V311.{}.{}{}number.kept.txt".format(SIZ,opo2,tpr2), "w") as f:
        number_kept_asvs = []
        for i in x_arr:
            print(i)
            val = sum(frq_cutoffs>=i)
            number_kept_asvs.append(val)
            f.write("{}\n".format(val))
else:
    with open("../data/V311.{}.{}{}number.kept.txt".format(SIZ,opo2,tpr2), "r") as f:
        number_kept_asvs = np.array([int(i.strip()) for i in f])
        
#Plot number of kept ASVs vs. cutoff for boundary value
frq_filt = int(FRQ)
fig, ax = plt.subplots()
ax.plot(x_arr, number_kept_asvs, linewidth=2, color="dodgerblue")
ax.fill_between(x_arr, 0, number_kept_asvs, color="dodgerblue", alpha=0.2)
ax.vlines(frq_filt,0,500, color="darkorange")
ax.hlines(number_kept_asvs[frq_filt],0,frq_filt, color="darkorange", linestyles="dashed")
ax.set_ylim(0,500)
ax.set_xlim(0,max(frq_cutoffs))
ax.set_xlabel("Cutoff (read counts)", fontsize=16)
ax.set_ylabel("#ASVs retained", fontsize=16)
fig.tight_layout()
fig.savefig("../figures/{}/V311.highpass.size.png".format(subdirec), format="png")
fig.clf()
