import pandas as pd
import numpy as np
import sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import itertools

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

##Prediction----------------------------------------------

#Range of years and months
#years = np.arange(2003,2022)
years = [2021]
months = np.arange(1,13)

for year, month in itertools.product(years, months):
	print(year, month)

	#Load satellite data
	DFgl_sat = pd.read_csv("../input/global/global_imputed_satellite_data.{}.{}.tsv".format(year,month), delimiter="\t", index_col=0, dtype="object").astype(float)
	print(DFgl_sat.shape)
	#Remove grid cells with missing values
	DFgl_sat_na = DFgl_sat.dropna()
	print(DFgl_sat_na.shape)
	#Get feature matrix
	X_global = DFgl_sat_na.loc[:,dico_feat_sel["satellite"]].values

	#Predict class probability with trained SVM
	y_global_proba = clr.predict_proba(X_global)
	#Make DataFrame of class probability
	DFp = pd.DataFrame(y_global_proba, index=DFgl_sat_na.index, columns=classes)
	#Probability scores under the cutoff -> nan
	DFp_b = (DFp > float(CTF)).astype(int)
	#Class with maximum probability -> predicted calss
	DFp_b["prediction"] = DFp.apply(lambda x: DFp.columns[np.argmax(x)], axis=1)
	#Save the prediction results
	DFp_b.to_csv("{}/global/global.prediction.{}.{}.tsv".format(subdirec,year,month), sep="\t")

