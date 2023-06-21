import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import label_binarize
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]
COM = sys.argv[6]
MLM = sys.argv[7]
CTF = sys.argv[8]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Loop by satellite feature sets
feature_sets = ["space","product","rrs","satellite","allfeat","sst"]
for fts in feature_sets:

	#Read the list of predicted class (= representative community) for each grids
	DFc = pd.read_csv("../data/{}/cv/prediction.spatial0.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Get the number of classes
	n_classes = max(DFc["class"])
	#Get the list of classes
	classes = [i for i in range(1,n_classes+1)]
	#Binarize the list of true class
	y_test = label_binarize(DFc["class"].values, classes=classes)	

	#Read the probabilistic output of the class prediction
	DFp = pd.read_csv("../data/{}/cv/probability.spatial0.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Binarize the probability matrix with given (optimized) threshold
	y_pred = (DFp > float(CTF)).astype(int).values

	#Make a metrics table
	DFmetrics = pd.DataFrame(index=["micro"]+classes, columns=["precision", "recall", "f1_score"])
	#Calculate micro-averaged precision, recall, and F-score
	DFmetrics.loc["micro","precision"] = precision_score(y_test.ravel(), y_pred.ravel())
	DFmetrics.loc["micro","recall"] = precision_score(y_test.ravel(), y_pred.ravel())
	DFmetrics.loc["micro","f1_score"] = f1_score(y_test.ravel(), y_pred.ravel())
	#Calculate precision, recall, and F-score for each class
	for i in range(n_classes):
		DFmetrics.loc[classes[i],"precision"] = precision_score(y_test[:, i], y_pred[:, i])
		DFmetrics.loc[classes[i],"recall"] = recall_score(y_test[:, i], y_pred[:, i])
		DFmetrics.loc[classes[i],"f1_score"]= f1_score(y_test[:, i], y_pred[:, i])

	#Save the metrics table
	DFmetrics.to_csv("../data/{}/V414.metrics.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), sep="\t")
