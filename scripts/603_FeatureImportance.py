import pandas as pd
import numpy as np
import sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]
COM = sys.argv[6]
MLM = sys.argv[7]
FTS = sys.argv[8]
CTF = sys.argv[9]

##Training-------------------------------------------------

#Define feature sets
dico_feat_sel = {}
dico_feat_sel["space"] = ["GridLat","GridLong_Sin","GridLong_Cos"]
dico_feat_sel["product"] = ["CHL_chlor_a", "KD490_Kd_490", "PIC_pic", "POC_poc", "PAR_par", "FLH_nflh", "SST"]
dico_feat_sel["rrs"] = ["RRS_Rrs_{}".format(i) for i in ["412","443","469","488","531","547","555","645","667","678"]]
dico_feat_sel["satellite"] = dico_feat_sel["product"] + dico_feat_sel["rrs"]
dico_feat_sel["allfeat"] = dico_feat_sel["space"] + dico_feat_sel["satellite"]
dico_feat_sel["sst"] = ["SST"]

#Load satellite data
DFs = pd.read_csv("../input/eukbank_imputed_satellite_data.tsv", delimiter="\t", index_col=0, dtype="object").astype(float)
#Convert circular feauture
DFs["GridLong_Sin"] = np.sin(np.pi*DFs["GridLong"]/180.)
DFs["GridLong_Cos"] = np.cos(np.pi*DFs["GridLong"]/180.)

#Load class data
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)
DFc = pd.read_csv("{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,COM), delimiter="\t", index_col=0)

#Get feature matrix
X = DFs.loc[DFc.index,dico_feat_sel[FTS]].values
#Get class vector
y = DFc["class"].values
#Get number of classes
n_classes = max(DFc["class"])
#Make a list of classes
classes = [i for i in range(1,n_classes+1)]

from sklearn.svm import SVC
#Make SVM instance
ml_inst = SVC(kernel='linear', C=1.0, probability=True, random_state=123, max_iter=-1)
clr = Pipeline([("sc", StandardScaler()),
                ("ml", ml_inst)])

#Train SVM
clr.fit(X, y)
print("Train Accuracy: {0:.3f}".format(clr.score(X, y)))

##Function for calculating feature importance--------------------------------
def IndivFeatImp(clr, X, y, scoring="accuracy", c=None, cutoff=None, folds=10, seed=0):

	#Get #samples and #features in data
	n_sample = X.shape[0]
	n_feat = X.shape[1]

	#Baseline score
	if c is None:
		if scoring != "accuracy":
			return Exception("Scoring should be 'accuracy' for whole prediction.")
		#For whole prediction
		#Get class prediction
		y_pred = clr.predict(X)
		#Calculate score
		baseline_score = accuracy_score(y, y_pred)	
	else:
		#For individual calss prediction
		#Binarize true class
		y_c = (y == c).astype(int)
		#Get individual prediction via probabilities
		y_prob = clr.predict_proba(X)
		y_prob_c = y_prob[:,c-1]
		#Calculate score
		if scoring == "accuracy":
			y_pred_c = (y_prob_c > cutoff).astype(int)
			baseline_score = accuracy_score(y_c, y_pred_c)
		elif scoring == "auc":
			baseline_score = roc_auc_score(y_c, y_prob_c)
		print("Baseline score of class {} ({}): {}".format(c, scoring, baseline_score))

	#Make a dataframe for saving results
	DFimp = pd.DataFrame()

	for fold in range(folds):

		#Generate permutated index
		rng = np.random.default_rng(seed=seed+fold)
		perm_index = rng.permutation(n_sample)

		#Loop by features
		list_imp = []
		for feat_ind in range(n_feat):
			#Copy data
			X_permutated = X.copy()
			#Permutate the column of given feature
			X_permutated[:,feat_ind] = X[perm_index,feat_ind]
			#Accuracy with permutated given feature
			if c is None:
				#For whole prediction
				#Get class prediction
				y_pred = clr.predict(X_permutated)
				#Calculate accuracy
				score = accuracy_score(y, y_pred)
			else:
				#For individual calss prediction
				#Get individual prediction via probabilities
				y_prob = clr.predict_proba(X_permutated)
				y_prob_c = y_prob[:,c-1]
				#Calculate score
				if scoring == "accuracy":
					y_pred_c = (y_prob_c > cutoff).astype(int)
					score = accuracy_score(y_c, y_pred_c)
				elif scoring == "auc":
					score = roc_auc_score(y_c, y_prob_c)
			#Add importance to the list
			list_imp.append(baseline_score-score)

		#Add the list of imprtances to the dataframe
		DFimp["fold_{}".format(fold)] = list_imp

	return DFimp

##Calculate summary statistics of whole/individual feature importance--------------------------------
DFwhole = IndivFeatImp(clr, X, y)
DFwhole_stat = pd.DataFrame({"importances_mean": DFwhole.mean(axis=1), "importances_std": DFwhole.std(axis=1)})
DFwhole_stat.index = dico_feat_sel[FTS]
DFwhole_stat.to_csv("{}/explore/feature.importance.myfunc.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,FTS), sep="\t")
for c in classes:
	#Accuracy
	DFindiv = IndivFeatImp(clr, X, y, c=c, cutoff=float(CTF))
	DFindiv_stat = pd.DataFrame({"importances_mean": DFindiv.mean(axis=1), "importances_std": DFindiv.std(axis=1)})
	DFindiv_stat.index = dico_feat_sel[FTS]	
	DFindiv_stat.to_csv("{}/explore/feature.importance.myfunc.{}.{}.{}.{}.{}.indiv{}.tsv".format(subdirec,NRM,COM,MLM,FTS,CTF,c), sep="\t")
	#ROC_AUC
	DFindiv = IndivFeatImp(clr, X, y, scoring="auc", c=c, cutoff=float(CTF))
	DFindiv_stat = pd.DataFrame({"importances_mean": DFindiv.mean(axis=1), "importances_std": DFindiv.std(axis=1)})
	DFindiv_stat.index = dico_feat_sel[FTS]
	DFindiv_stat.to_csv("{}/explore/feature.importance.myfunc.{}.{}.{}.{}.{}.auc.indiv{}.tsv".format(subdirec,NRM,COM,MLM,FTS,CTF,c), sep="\t")

