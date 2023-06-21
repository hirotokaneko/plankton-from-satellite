import pandas as pd
import matplotlib.pyplot as plt
import sys
import geopandas as gpd
from shapely.geometry import Point

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]
COM = sys.argv[6]
MLM = sys.argv[7]
CTF = sys.argv[8]

#Get the world map
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
#Read the list of grids
DFg = pd.read_csv("../data/eukbank_satellite_grid.tsv", delimiter="\t", index_col=0)

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Loop by satellite feature sets
feature_sets = ["space","product","rrs","satellite","allfeat","sst","chl","par","duo","trio"]
for fts in feature_sets:

	#Read the list of predicted class (= representative community) for each grids
	DFc = pd.read_csv("../data/{}/cv/prediction.spatial0.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Read the probabilistic output of the class prediction
	DFp = pd.read_csv("../data/{}/cv/probability.spatial0.{}.{}.{}.{}.tsv".format(subdirec,NRM,COM,MLM,fts), delimiter="\t", index_col=0)
	#Binarize the list of true class
	DFp_b = (DFp > float(CTF)).astype(int)

	#Classify the success or failure of prediction
	DFresult = pd.DataFrame(index=DFc.index)
	for i in DFc.index:
		true_class = DFc.loc[i,"class"]
		if DFp_b.loc[i,str(true_class)] == 1:
			if DFp_b.loc[i,:].sum() == 1:
				DFresult.loc[i,"result"] = "correct"
			else:
				DFresult.loc[i,"result"] = "partially correct"
		else:
			if DFp_b.loc[i,:].sum() == 0:
				DFresult.loc[i,"result"] = "no prediction"
			else:
				DFresult.loc[i,"result"] = "wrong"

	#Count the number of prediction success/failure values
	result_counts = DFresult.value_counts()
	print(result_counts)
	#Add prediction success/failure value to the list of grids
	DFcat = pd.concat([DFg, DFresult], axis=1, join="inner")

	#Convert into GeoDataFrame
	geometry = [Point(xy) for xy in zip(DFcat["GridLong"], DFcat["GridLat"])]
	DFcoords = gpd.GeoDataFrame(DFcat, crs="EPSG:4326", geometry=geometry)

	#List of the success/failure values and their color
	result_types = ["correct","partially correct","wrong","no prediction"]
	colors = {"correct":"blue","partially correct":"purple","wrong":"red","no prediction":"darkgrey"}
	#Make a subplot
	fig, ax = plt.subplots(figsize=(10,5))
	#Plot the world map
	base = countries.plot(ax=ax, color="darkgrey")
	#Plot the locations of samples colored by prediction success/failure values
	for t in [i for i in result_types if i in result_counts.index]:
		label = "{} (n = {})".format(t, result_counts[t])
		DFcoords[DFcoords["result"]==t].plot(ax=base, markersize=10, color=colors[t], edgecolor="grey", linewidth=1, label=label)
	#Add legend
	ax.legend(loc="upper right")
	#Save to a PNG file
	fig.tight_layout()
	fig.savefig("../figures/{}/cv/V413.prediction.map.spatial0.{}.{}.{}.{}.png".format(subdirec,NRM,COM,MLM,fts), format="png")
	plt.close(fig)
