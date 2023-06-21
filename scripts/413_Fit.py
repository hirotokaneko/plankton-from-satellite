import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

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
#Convert circular features
DFs["GridLong_Sin"] = np.sin(np.pi*DFs["GridLong"]/180.)
DFs["GridLong_Cos"] = np.cos(np.pi*DFs["GridLong"]/180.)

#Load class data
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)
DFc = pd.read_csv("{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,COM), delimiter="\t", index_col=0)

#Make matrix and vector
X = DFs.loc[DFc.index,dico_feat_sel[FTS]].values
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

elif MLM == "SVM":
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

##Fit hyperparameters using all samples-----------------------------------

#Standardize features if non-tree-based methods will be used
if MLM == "RF":
	clr = Pipeline([("ml", ml_inst)])
else:
	clr = Pipeline([("sc", StandardScaler()), ("ml", ml_inst)])

#Grid search 5-fold CV
gs = GridSearchCV(estimator=clr, param_grid=param_grid, scoring="accuracy", cv=5, n_jobs=int(JOB), return_train_score=True)
gs.fit(X, y)
#Save fit result
DFgs = pd.DataFrame(gs.cv_results_)
DFgs.to_csv("{}/fit/gridsearch.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,FTS), sep="\t")

#Get best predictor
clr_best = gs.best_estimator_
print("Best estimator:")
print(clr_best)
print()

#Get feature importances
result = permutation_importance(clr_best, X, y, n_repeats=5, random_state=123)
DFimp = pd.DataFrame({"importances_mean": result["importances_mean"], "importances_std": result["importances_std"]}, index=dico_feat_sel[FTS])
#
DFimp.to_csv("{}/fit/feature.importance.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,FTS), sep="\t")

