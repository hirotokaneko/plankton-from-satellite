import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score, PrecisionRecallDisplay
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
RAD = sys.argv[8]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Loop by satellite feature sets
feature_sets = ["space","product","rrs","satellite","allfeat","sst","chl","par","duo","trio"]
for fts in feature_sets:

	#----------------------
	# Plot confusion matrix
	#----------------------

	#Read the list of predicted class (= representative community) for each grids
	DFc = pd.read_csv("../data/{}/cv/prediction.spatial{}.{}.{}.{}.{}.tsv".format(subdirec,RAD,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Get the number of classes
	n_classes = max(DFc["class"])
	#Get the list of classes
	classes = [i for i in range(1,n_classes+1)]

	#Plot confusion matrix
	confmat = confusion_matrix(DFc["class"], DFc["predicted"], labels=classes)
	fig, ax = plt.subplots(figsize=(7,5))
	ax.matshow(confmat, cmap=plt.cm.Blues)
	for i in range(confmat.shape[0]):
		for j in range(confmat.shape[1]):
			ax.text(x=j, y=i, s=confmat[i,j], va="center", ha="center", fontsize=14)
	ax.set_xlabel("Predicted comm. type", fontsize=16)
	ax.set_ylabel("True comm. type", fontsize=16)
	ax.xaxis.tick_top()
	ax.xaxis.set_label_position("top")
	ax.set_xticks(np.arange(len(classes)))
	ax.set_xticklabels(classes, fontsize=14)
	ax.set_yticks(np.arange(len(classes)))
	ax.set_yticklabels(classes, fontsize=14)
	fig.tight_layout()
	fig.savefig("../figures/{}/cv/V411.confusion.matrix.spatial{}.{}.{}.{}.{}.png".format(subdirec,RAD,NRM,COM,MLM,fts), format="png")
	plt.close(fig)

	#----------------------

	#----------------------
	# Plot ROC curve
	#----------------------

	#Read the probabilistic output of the class prediction
	DFp = pd.read_csv("../data/{}/cv/probability.spatial{}.{}.{}.{}.{}.tsv".format(subdirec,RAD,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Binarize the list of true class
	y_test = label_binarize(DFc["class"].values, classes=classes)
	#Get the probability matrix
	y_score = DFp.values

	#Calculate ROC curve and AUC for each class
	fpr, tpr, thresholds, roc_auc = {}, {}, {}, {}
	for i in range(n_classes):
		fpr[classes[i]], tpr[classes[i]], thresholds[classes[i]] = roc_curve(y_test[:, i], y_score[:, i])
		roc_auc[classes[i]] = auc(fpr[classes[i]], tpr[classes[i]])

	#Calculate micro-averaged ROC curve and AUC
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

	#Collect all FPR values
	all_fpr = np.unique(np.concatenate([fpr[i] for i in classes]))
	#Get TPR values corresponded to FPR values by interpolation
	mean_tpr = np.zeros_like(all_fpr)
	for i in classes:
		mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
	#Calculate macro-averaged ROC curve and AUC
	mean_tpr /= n_classes
	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

	#Make a subplot
	fig, ax = plt.subplots(figsize=(7,5))
	#Plot micro-averaged ROC curve
	ax.plot(fpr["micro"], tpr["micro"],
		label="Micro-avg. AUC = {0:0.2f}".format(roc_auc["micro"]),
		color="deeppink", linestyle=":", linewidth=4)
	#Plot macro-averaged ROC curve
	ax.plot(fpr["macro"], tpr["macro"],
		label="Macro-avg. AUC = {0:0.2f}".format(roc_auc["macro"]),
		color="navy", linestyle=":", linewidth=4)
	#Plot ROC curve of each class
	for i in classes:
		ax.plot(fpr[i], tpr[i], color=cm.jet(i/float(n_classes)), lw=2,
			label="Comm. type {0} AUC = {1:0.2f}".format(i, roc_auc[i]))
	#Plot perfect prediction
	ax.plot([0, 1], [0, 1], "k--", lw=2)
	#Set labels
	tks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
	labs = [str(i) for i in tks]
	ax.set_xticks(tks)
	ax.set_yticks(tks)
	ax.set_xticklabels(labs, fontsize=14)
	ax.set_yticklabels(labs, fontsize=14)
	ax.set_xlim([0.0, 1.0])
	ax.set_ylim([0.0, 1.05])
	ax.set_xlabel("False Positive Rate", fontsize=16)
	ax.set_ylabel("True Positive Rate", fontsize=16)
	ax.legend(loc="lower right", fontsize=14)
	fig.tight_layout()
	#Save to a PNG file
	fig.savefig("../figures/{}/cv/V411.ROCcurve.spatial{}.{}.{}.{}.{}.png".format(subdirec,RAD,NRM,COM,MLM,fts), format="png")
	plt.close(fig)

	#----------------------

	#----------------------
	# Plot precision-recall curve
	#----------------------

	#Calculate precision and recall for each class
	precision, recall, average_precision = {}, {}, {}
	for i in range(n_classes):
		precision[classes[i]], recall[classes[i]], _ = precision_recall_curve(y_test[:, i], y_score[:, i])
		average_precision[classes[i]] = average_precision_score(y_test[:, i], y_score[:, i])

	#Calculate micro-averaged precision and recall
	precision["micro"], recall["micro"], thresholds = precision_recall_curve(y_test.ravel(), y_score.ravel())
	average_precision["micro"] = average_precision_score(y_test, y_score, average="micro")

	#Make a subplot
	fig, ax = plt.subplots(figsize=(7,5))
	#Plot the iso-F-score curves
	f_scores = np.linspace(0.2, 0.8, num=4)
	lines, labels = [], []
	for f_score in f_scores:
		x = np.linspace(0.01, 1)
		y = f_score * x / (2 * x - f_score)
		ax.plot(x[y >= 0], y[y >= 0], color="gray", alpha=0.2)
		ax.text(0.9, y[45] + 0.02, "f1={0:0.1f}".format(f_score), fontsize=14)
	#Plot micro-averaged PR curve
	display = PrecisionRecallDisplay(recall=recall["micro"], precision=precision["micro"],
    	average_precision=average_precision["micro"])
	display.plot(ax=ax, name="Micro-avg.", color="gold")
	#Plot PR curve of each class
	for i in classes:
		display = PrecisionRecallDisplay(recall=recall[i], precision=precision[i],
			average_precision=average_precision[i])
		display.plot(ax=ax, name="Comm. type {}".format(i), color=cm.jet(i/float(n_classes)))
	#Set labels
	tks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
	labs = [str(i) for i in tks]
	ax.set_xticks(tks)
	ax.set_yticks(tks)
	ax.set_xticklabels(labs, fontsize=14)
	ax.set_yticklabels(labs, fontsize=14)
	ax.set_xlim([0.0, 1.0])
	ax.set_ylim([0.0, 1.05])
	ax.set_xlabel("Recall", fontsize=16)
	ax.set_ylabel("Precision", fontsize=16)
	ax.legend(loc="lower left")
	fig.tight_layout()
	#Save to a PNG file
	fig.savefig("../figures/{}/cv/V411.PRcurve.spatial{}.{}.{}.{}.{}.png".format(subdirec,RAD,NRM,COM,MLM,fts), format="png")
	plt.close(fig)

	#----------------------

	#----------------------
	# Plot F-score with changing threshold
	#----------------------

	#Claculate F-score with micro-averaged precision and recall
	prod_rec_pre = recall["micro"][:-1]*precision["micro"][:-1]
	sum_rec_pre = recall["micro"][:-1]+precision["micro"][:-1]
	f1_scores = 2*np.divide(prod_rec_pre, sum_rec_pre, out=np.zeros_like(prod_rec_pre), where=sum_rec_pre!=0)
	#Get the maximum F-score
	max_f1 = np.max(f1_scores)
	#Get the threshold providing the maximum F-score
	max_threshold = thresholds[np.argmax(f1_scores)]

	#Plot F-score with changing threshold
	fig, ax = plt.subplots(figsize=(7,5))
	ax.plot(thresholds, f1_scores, c="blue")
	ax.vlines(max_threshold, 0.0, 1.0, colors="darkorange")
	ax.text(max_threshold, max_f1, "max f1 = {0:.2f} at threshold {1:.2f}".format(max_f1, max_threshold), fontsize=14)
	#Set labels
	tks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
	labs = [str(i) for i in tks]
	ax.set_xticks(tks)
	ax.set_yticks(tks)
	ax.set_xticklabels(labs, fontsize=14)
	ax.set_yticklabels(labs, fontsize=14)
	ax.set_xlim([0.0, 1.0])
	ax.set_ylim([0.0, 1.0])
	ax.set_xlabel("Threshold", fontsize=16)
	ax.set_ylabel("F1 score", fontsize=16)
	fig.tight_layout()
	#Save to a PNG file
	fig.savefig("../figures/{}/cv/V411.Fscore.spatial{}.{}.{}.{}.{}.png".format(subdirec,RAD,NRM,COM,MLM,fts), format="png")
	plt.close(fig)

	#----------------------
