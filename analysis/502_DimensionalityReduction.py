import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import umap
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
AAJ = sys.argv[5]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Dictionary of satellite feature sets
dico_feat_sel = {}
dico_feat_sel["space"] = ["GridLat","GridLong_Sin","GridLong_Cos"]
dico_feat_sel["product"] = ["CHL_chlor_a", "KD490_Kd_490", "PIC_pic", "POC_poc", "PAR_par", "FLH_nflh", "SST"]
dico_feat_sel["rrs"] = ["RRS_Rrs_{}".format(i) for i in ["412","443","469","488","531","547","555","645","667","678"]]
dico_feat_sel["satellite"] = dico_feat_sel["product"] + dico_feat_sel["rrs"]
dico_feat_sel["allfeat"] = dico_feat_sel["space"] + dico_feat_sel["satellite"]

#Read the satellite data of random grids
DFsat = pd.read_csv("../input/random_imputed_satellite_data.tsv", delimiter="\t", index_col=0)
#Read the random grid data
DFg = pd.read_csv("../input/random_satellite_grid.elev.minus.prov.tsv", delimiter="\t", index_col=0)

#Convert circular feauture
DFsat["GridLong_Sin"] = np.sin(np.pi*DFsat["GridLong"]/180.)
DFsat["GridLong_Cos"] = np.cos(np.pi*DFsat["GridLong"]/180.)

#Get the grid index of "open ocean" (sea floor depth > 200 m)
if OPO == "open":
	index_openocean = DFg.index[DFg["elevation"] <= -200]
else:
	index_openocean = DFg.index

#Extract "open ocean" rows
DFsat_open = DFsat.loc[index_openocean, :]
#Drop rows with missing values
DFsat_open_dr = DFsat_open.dropna()

#Area adjustment of random grids
if AAJ == "adjusted":
	#Get cosine of latitude (= relative area to equatorial grids)
	cosine_vals = np.cos(np.deg2rad(DFsat["GridLat"]))
	#Generate random values between 0 and 1
	rng = np.random.default_rng(seed=123)
	random_vals = rng.random(DFsat.shape[0])
	#Get coodinate index of cosine > random value
	index_latadj = DFsat.index[cosine_vals > random_vals]
	#Get selected coordinates in data index
	index_latadj_comp = [i for i in index_latadj if i in DFsat_open_dr.index]
	#Get satellite data of area adjusted random grids
	DFsat_prep = DFsat_open_dr.loc[index_latadj_comp, :]
else:
	DFsat_prep = DFsat_open_dr
#Write prepared satellite data
DFsat_prep.to_csv("random_imputed_satellite_data.4umap.{}.tsv".format(AAJ), sep="\t")

#Read the satellite data of EukBank grids
DFeuks = pd.read_csv("../input/eukbank_imputed_satellite_data.tsv", delimiter="\t", index_col=0)
#Read the satellite data of EukBank grids
DFeuks["GridLong_Sin"] = np.sin(np.pi*DFeuks["GridLong"]/180.)
DFeuks["GridLong_Cos"] = np.cos(np.pi*DFeuks["GridLong"]/180.)

#Read the frequency table
DFf = pd.read_csv("{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), delimiter="\t", index_col=0)

#Loop by satellite feature sets
feature_sets = ["space","product","rrs","satellite","allfeat"]
for fts in feature_sets:
	print(">>", fts)

	#Convert satellite data to matrix
	X = DFsat_prep.loc[:,dico_feat_sel[fts]].values
	Xeuk = DFeuks.loc[DFf.index,dico_feat_sel[fts]].values

	#Standardize satellite features
	sc = StandardScaler()
	X_sc = sc.fit_transform(X)
	Xeuk_sc = sc.transform(Xeuk)

	print("U-map")
	#Dimension reduction with UMAP
	emmb = umap.UMAP(random_state=123)
	X_sc_emmb = emmb.fit_transform(X_sc)
	Xeuk_sc_emmb = emmb.transform(Xeuk_sc)
		
	#Save the UMAP projections (first and second dimension) to the file
	DFsc_emmb = pd.DataFrame(X_sc_emmb, index=DFsat_prep.index, columns=["Umap 1", "Umap 2"])
	DFeuk_sc_emmb = pd.DataFrame(Xeuk_sc_emmb, index=DFf.index, columns=["Umap 1", "Umap 2"])
	DFsc_emmb.to_csv("{}/umap/umap.random.{}.{}.tsv".format(subdirec, AAJ, fts), sep="\t")
	DFeuk_sc_emmb.to_csv("{}/umap/umap.eukbank.{}.{}.tsv".format(subdirec, AAJ, fts), sep="\t")

