import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]
COM = sys.argv[6]
MLM = sys.argv[7]
FTS = sys.argv[8]
JOB = sys.argv[9]
LIM = sys.argv[10]
RAD = sys.argv[11]

##----------------------------------------
#Define feature sets
dico_feat_sel = {}
dico_feat_sel["space"] = ["GridLat","GridLong_Sin","GridLong_Cos"]
dico_feat_sel["product"] = ["CHL_chlor_a", "KD490_Kd_490", "PIC_pic", "POC_poc", "PAR_par", "FLH_nflh", "SST"]
dico_feat_sel["rrs"] = ["RRS_Rrs_{}".format(i) for i in ["412","443","469","488","531","547","555","645","667","678"]]
dico_feat_sel["satellite"] = dico_feat_sel["product"] + dico_feat_sel["rrs"]
dico_feat_sel["allfeat"] = dico_feat_sel["space"] + dico_feat_sel["satellite"]
dico_feat_sel["sst"] = ["SST"]
dico_feat_sel["chl"] = ["CHL_chlor_a"]
dico_feat_sel["par"] = ["PAR_par"]
dico_feat_sel["duo"] = ["SST", "CHL_chlor_a"]
dico_feat_sel["trio"] = ["SST", "CHL_chlor_a", "PAR_par"]

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
print("#samples: {}".format(DFc.shape[0]))

#Load grid distance
DFd = pd.read_csv("../input/eukbank_grid_distance.tsv", delimiter="\t", index_col=0)

#Get feature matrix
X = DFs.loc[DFc.index,dico_feat_sel[FTS]].values
#Get class vector
y = DFc["class"].values

#Make ML instance
if MLM == "NB":
        from sklearn.naive_bayes import GaussianNB
        ml_inst = GaussianNB()
        param_range = np.logspace(-4,3,8)
        param_grid = [{"ml__var_smoothing": param_range}]

elif MLM == "KNN":
        from sklearn.neighbors import KNeighborsClassifier
        ml_inst = KNeighborsClassifier()
        param_range = np.arange(1,10,1)
        param_grid = [{"ml__n_neighbors": param_range}]

if MLM == "SVM":
        from sklearn.svm import SVC
        ml_inst = SVC(random_state=123, probability=True, max_iter=-1)
        param_range = np.logspace(-4,3,8)
        param_grid = [{"ml__C": param_range,
                       "ml__kernel": ["linear"]},
                      {"ml__C": param_range,
                       "ml__gamma": param_range,
                       "ml__kernel": ["rbf"]}]

elif MLM == "NN":
        from sklearn.neural_network import MLPClassifier
        ml_inst = MLPClassifier(solver="lbfgs", random_state=123, max_iter=10**int(LIM))
        param_range = np.logspace(-6,3,10)
        param_layer = [(i) for i in np.arange(10,50,10)]
        param_grid = {"ml__alpha": param_range,
                      "ml__activation": ["identity","logistic","tanh","relu"],
                      "ml__hidden_layer_sizes": param_layer}

elif MLM == "RF":
        from sklearn.ensemble import RandomForestClassifier
        ml_inst = RandomForestClassifier(random_state=123)
        param_range = np.array([10,100,1000,10000])
        param_grid = {"ml__n_estimators": param_range}

##Spatial nested CV-----------------------------------

#Standardize features if non-tree-based methods will be used
if MLM == "RF":
	clr = Pipeline([("ml", ml_inst)])
else:
	clr = Pipeline([("sc", StandardScaler()), ("ml", ml_inst)])

#Data frame for prediction results
DFpred = pd.DataFrame(DFc["class"])
DFproba = pd.DataFrame(index=DFc.index, columns=DFc.columns[:-1])

#Radius for bufferd CV
radius = int(RAD)*1000

#CV
for test_index, test_sample in enumerate(DFc.index):
	print("outer cv (leave-one-out): sample {}".format(test_index))

	#Non-neighbour samples 
	out_sample = DFd.index[DFd.loc[test_sample,:] > radius]
	#Training samples
	train_sample = set(DFc.index)&set(out_sample)
	#Index for training samples
	train_index = [i for i, s in enumerate(DFc.index) if s in train_sample]

	#Split data into training and test
	X_train, X_test = X[train_index,:], X[test_index,np.newaxis]
	y_train, y_test = y[train_index], y[test_index]

	#Grid search (inner cv)
	gs = GridSearchCV(estimator=clr, param_grid=param_grid, scoring="accuracy",
			  return_train_score=True, cv=2, n_jobs=int(JOB))
	#Fit hyperparameters
	gs.fit(X_train, y_train)

	#Get best predictor
	clr_best = gs.best_estimator_
	print("best estimator: {}".format(clr_best))
    
	#Predict test sample using best predictor
	clr_best.fit(X_train, y_train)
	y_test_pred = clr_best.predict(X_test)
	y_test_proba = clr_best.predict_proba(X_test)

	#Save prediction results
	DFpred.loc[test_sample,"predicted"] = y_test_pred
	DFproba.loc[test_sample,:] = y_test_proba

#Print CV accuracy
print("Leave-one-out CV accuracy: {}".format(accuracy_score(DFpred["class"], DFpred["predicted"])))
#Save tables of prediction results
DFpred.to_csv("{}/cv/prediction.spatial{}.{}.{}.{}.{}.tsv".format(subdirec,RAD,NRM,COM,MLM,FTS), sep="\t")
DFproba.to_csv("{}/cv/probability.spatial{}.{}.{}.{}.{}.tsv".format(subdirec,RAD,NRM,COM,MLM,FTS), sep="\t")

