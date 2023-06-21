import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]
COM = sys.argv[6]
MLM = sys.argv[7]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Name of satellite features for labels
FeatNames = {"GridLat": "Lat",
			 "GridLong_Sin": "Long (sin)",
			 "GridLong_Cos": "Long (cos)",
			 "CHL_chlor_a": "CHL",
			 "KD490_Kd_490": "KD490",
			 "PIC_pic": "PIC",
			 "POC_poc": "POC",
			 "PAR_par": "PAR",
			 "FLH_nflh": "FLH",
			 "SST": "SST",
			 "RRS_Rrs_412": "RRS(412)",
			 "RRS_Rrs_443": "RRS(443)",
			 "RRS_Rrs_469": "RRS(469)",
			 "RRS_Rrs_488": "RRS(488)",
			 "RRS_Rrs_531": "RRS(531)",
			 "RRS_Rrs_547": "RRS(547)",
			 "RRS_Rrs_555": "RRS(555)",
			 "RRS_Rrs_645": "RRS(645)",
			 "RRS_Rrs_667": "RRS(667)",
			 "RRS_Rrs_678": "RRS(678)"}

#Labels for hyperparameter
HPset = {"KNN": ("Number of neighbors", [str(i) for i in range(1,10)]),
		 "NB": ("Smoothing papameter", ["$10^{"+str(i)+"}$" for i in range(-4,4)]),
		 "NN": ("Activation function - Hidden layer size",
		 ["identity - {}".format(i) for i in [10,20,30,40]] + ["logistic - {}".format(i) for i in [10,20,30,40]] +
		 ["ReLU - {}".format(i) for i in [10,20,30,40]] + ["tanh - {}".format(i) for i in [10,20,30,40]]),
		 "RF": ("Number of trees", [str(10**i) for i in range(1,5)]),
		 "SVM": ("Kernel", ["linear"]+["RBF (coef = $10^{"+str(i)+"}$)" for i in range(-4,4)])}

#Loop by satellite feature sets
feature_sets = ["space","product","rrs","satellite","allfeat","sst","chl","par","duo","trio"]
for fts in feature_sets:

 	#----------------------
	#Plot feature impotance
	#----------------------

	#Read the table of feature impotance
	DFimp = pd.read_csv("../data/{}/fit/feature.importance.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), delimiter="\t",index_col=0)
	#Plot the feature impotance
	fig, ax = plt.subplots(figsize=(7,5))
	ax.bar(np.arange(DFimp.shape[0]), DFimp["importances_mean"], yerr=DFimp["importances_std"])
	ax.set_xticks(np.arange(DFimp.shape[0]))
	ax.set_xticklabels([FeatNames[i] for i in DFimp.index], rotation=90, fontsize=14)
	ax.tick_params(labelsize=14)
	fig.tight_layout()
	fig.savefig("../figures/{}/fit/V412.feature.importance.{}.{}.{}.{}.png".format(subdirec,NRM,COM,MLM,fts), format="png")
	plt.close(fig)

	#----------------------

	#----------------------
	# Plot grid search results
	#----------------------

	#Read the table of grid search results
	DFgs = pd.read_csv("../data/{}/fit/gridsearch.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Number of fold
	fold=5
	#Sort rows
	if MLM == "NN":
		DFgs = DFgs.sort_values(by=["param_ml__activation","param_ml__hidden_layer_sizes","param_ml__alpha"])
	if MLM == "SVM":
		DFgs = DFgs.sort_values(by=["param_ml__kernel","param_ml__gamma","param_ml__C"])
	print(DFgs["params"])
	#Make a subplot
	figw = {"KNN": 7, "NB": 7, "NN": 12, "SVM": 9, "RF": 7}
	fig, ax = plt.subplots(figsize=(figw[MLM],5))
	#Get the number of rows
	num = DFgs.shape[0]
	#Get the mean and standard error of test and training accuracies
	mean_tests, std_tests = DFgs["mean_test_score"].astype(float), DFgs["std_test_score"].astype(float)/np.sqrt(fold)
	mean_trains, std_trains = DFgs["mean_train_score"].astype(float), DFgs["std_train_score"].astype(float)/np.sqrt(fold)
	#Plot test and training accuracies with error bars
	ax.errorbar(x=np.arange(num), y=mean_tests, yerr=std_tests, color="blue", lw=2)
	ax.errorbar(x=np.arange(num), y=mean_trains, yerr=std_trains, color="orange", lw=2)
	#Highlight the maximum test accuracy
	ax.hlines(y=np.max(mean_tests), xmin=-(num-1)*0.1, xmax=(num-1)*1.1, colors=["grey"], lw=1.5, ls="--")
	ax.vlines(x=np.argmax(mean_tests), ymin=0, ymax=1.2, colors=["grey"], lw=1.5, ls="--")
	#Set ticks
	tks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
	ax.set_yticks(tks)
	labs = [str(i) for i in tks]
	ax.set_yticklabels(labs, fontsize=18)
	if MLM == "NN":
		ax.set_xticks(np.arange(5,num,10))
		ax.set_xticklabels(HPset[MLM][1], fontsize=15, rotation=90)
	elif MLM == "SVM":
		ax.set_xticks(np.arange(4,num,8))
		ax.set_xticklabels(HPset[MLM][1], fontsize=15, rotation=90)
	else:
		ax.set_xticks(np.arange(num))
		ax.set_xticklabels(HPset[MLM][1], fontsize=18)
	#Set limits
	ax.set_ylim(0,1.2)
	mergin = 0.05 if MLM in ["SVM", "NN"] else 0.1
	ax.set_xlim(-(num-1)*mergin,(num-1)*(1+mergin))
	#Set labels
	ax.set_ylabel("Training/test accuracy", fontsize=18)
	ax.set_xlabel(HPset[MLM][0], fontsize=18)
	#Save to a PNG file
	fig.tight_layout()
	fig.savefig("../figures/{}/fit/V412.gridsearch.{}.{}.{}.{}.png".format(subdirec,NRM,COM,MLM,fts), format="png")
	plt.close(fig)

	#----------------------
