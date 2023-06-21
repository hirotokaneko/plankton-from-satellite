import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Name of satellite features for labels
FeatNames = {"GridLat": "Lat",
			 "GridLong_Sin": "Long (sin)",
			 "GridLong_Cos": "Long (cos)",
			 "CHL_chlor_a": "Chl a",
			 "KD490_Kd_490": "Kd(490)",
			 "PIC_pic": "PIC",
			 "POC_poc": "POC",
			 "PAR_par": "PAR",
			 "FLH_nflh": "nFLH",
			 "SST": "SST",
			 "RRS_Rrs_412": "Rrs(412)",
			 "RRS_Rrs_443": "Rrs(443)",
			 "RRS_Rrs_469": "Rrs(469)",
			 "RRS_Rrs_488": "Rrs(488)",
			 "RRS_Rrs_531": "Rrs(531)",
			 "RRS_Rrs_547": "Rrs(547)",
			 "RRS_Rrs_555": "Rrs(555)",
			 "RRS_Rrs_645": "Rrs(645)",
			 "RRS_Rrs_667": "Rrs(667)",
			 "RRS_Rrs_678": "Rrs(678)"}

#Read the feature importance for whole prediction
DFwhole = pd.read_csv("../data/{}/explore/feature.importance.myfunc.fz.leiden.SVM.satellite.tsv".format(subdirec), delimiter="\t", index_col=0)
#Read the feature importance for whole prediction (sk-laern)
DFsk = pd.read_csv("../data/{}/fit/feature.importance.fz.leiden.SVM.satellite.tsv".format(subdirec), delimiter="\t", index_col=0)

#Plot feature importance for whole prediction (in-house function vs sk-learn）
fig, axes = plt.subplots(1, 2, figsize=(10,5))
for i, DFtmp in enumerate([DFwhole, DFsk]):
    ax = axes[i]
    ax.bar(np.arange(DFtmp.shape[0]), DFtmp["importances_mean"], yerr=DFtmp["importances_std"])
    ax.set_xticks(np.arange(DFtmp.shape[0]))
    ax.set_xticklabels([FeatNames[i] for i in DFtmp.index], rotation=90, fontsize=14)
    ax.tick_params(labelsize=14)
axes[0].set_title("In-house function", fontsize=16)
axes[1].set_title("Scikit-learn function", fontsize=16)
fig.tight_layout()
fig.savefig("../figures/{}/explore/V602.feature.importance.comparison.png".format(subdirec), format="png")
plt.close(fig)

#Load class data
DFc = pd.read_csv("../data/{}/edge.satisfaction.{}.{}{}frq{}.fz.leiden.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), delimiter="\t", index_col=0)
#Get number of classes
n_classes = max(DFc["class"])
#Make a list of classes
classes = [i for i in range(1,n_classes+1)]

#Accuracy
#Make a subplots
fig, axes = plt.subplots(2, 3, figsize=(18,10), sharex=True)
#Loop by classes
for c in classes:
        
	#Set subplot
	ax = axes[(c-1)//3,(c-1)%3]
	#Read the feature importance for individual prediction
	DFindiv = pd.read_csv("../data/{}/explore/feature.importance.myfunc.fz.leiden.SVM.satellite.0.28.indiv{}.tsv".format(subdirec, c), delimiter="\t", index_col=0)
	#Plot feature importance for individual prediction
	ax.bar(np.arange(DFindiv.shape[0]), DFindiv["importances_mean"], yerr=DFindiv["importances_std"])
	ax.hlines(0.0, -0.7, DFindiv.shape[0]-0.3, colors="grey", linewidth=1)
	ax.tick_params(labelsize=14)
	ax.set_xticks(np.arange(DFindiv.shape[0]))
	ax.set_xticklabels([FeatNames[i] for i in DFindiv.index], rotation=90, fontsize=14)
	ax.tick_params(labelsize=14)
	ax.set_ylim(-0.07,0.24)
	ax.set_xlim(-0.7, DFindiv.shape[0]-0.3)
	ax.set_title("Community type {}".format(c), fontsize=18)

fig.tight_layout()
fig.savefig("../figures/{}/explore/V602.feature.importance.indiv.png".format(subdirec), format="png")
plt.close(fig)

#ROC-AUC
#Make a subplots
fig, axes = plt.subplots(2, 3, figsize=(18,10), sharex=True)
#Loop by classes
for c in classes:
        
        #Set subplot
        ax = axes[(c-1)//3,(c-1)%3]
        #Read the feature importance for individual prediction
        DFindiv = pd.read_csv("../data/{}/explore/feature.importance.myfunc.fz.leiden.SVM.satellite.0.28.auc.indiv{}.tsv".format(subdirec, c), delimiter="\t", index_col=0)
        #Plot feature importance for individual prediction
        ax.bar(np.arange(DFindiv.shape[0]), DFindiv["importances_mean"], yerr=DFindiv["importances_std"])
        ax.hlines(0.0, -0.7, DFindiv.shape[0]-0.3, colors="grey", linewidth=1)
        ax.tick_params(labelsize=14)
        ax.set_xticks(np.arange(DFindiv.shape[0]))
        ax.set_xticklabels([FeatNames[i] for i in DFindiv.index], rotation=90, fontsize=14)
        ax.tick_params(labelsize=14)
        ax.set_ylim(-0.05,0.3)
        ax.set_xlim(-0.7, DFindiv.shape[0]-0.3)
        ax.set_title("Community type {}".format(c), fontsize=18)

fig.tight_layout()
fig.savefig("../figures/{}/explore/V602.feature.importance.auc.indiv.png".format(subdirec), format="png")
plt.close(fig)

