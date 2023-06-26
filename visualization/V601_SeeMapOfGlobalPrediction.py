import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as mpatches
import geopandas as gpd
from shapely.geometry import Point
import sys
import itertools

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Get the world map
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

#Read the list of grids
DFg = pd.read_csv("../input/global/global_imputed_satellite_data.2021.1.tsv", delimiter="\t", index_col=0).iloc[:,-2:]

#List of years and months
years = [2021] #for test
#years = np.arange(2003,2022)
months = np.arange(1,13)

#Loop by years and months
for year, month in itertools.product(years, months):
	print(year, month)

	#Read the table of the predicted class (= representative community) in given month/year
	DFp = pd.read_csv("../data/{}/global/global.prediction.{}.{}.tsv".format(subdirec,year,month), delimiter="\t", index_col=0)
	DFpb = DFp.iloc[:,:-1]

	#Index classified by the number of predicted classes
	index_none = DFpb.index[DFpb.sum(axis=1) == 0]
	index_single = DFpb.index[DFpb.sum(axis=1) == 1]
	index_multi = DFpb.index[DFpb.sum(axis=1) > 1]

	#Add winner class (= claas with highest probability) to the list of grids
	DFcat = pd.concat([DFg, DFp["prediction"]], axis=1, join="inner")

	#Convert into GeoDataFrame
	geometry = [Point(xy) for xy in zip(DFcat["GridLong"], DFcat["GridLat"])]
	DFcoords = gpd.GeoDataFrame(DFcat, crs="EPSG:4326", geometry=geometry)

	#Make a subplot
	fig, ax = plt.subplots(figsize=(8,4.5))
	base = countries.plot(ax=ax, color="grey")
	n_com = DFpb.shape[1]
	#Cut the table by the number of predicted class
	DFnone = DFcoords.loc[index_none,:]
	DFsingle = DFcoords.loc[index_single,:]
	DFmulti = DFcoords.loc[index_multi,:]
	#Plot grids without predicted class in grey
	DFnone.plot(ax=base, markersize=1, color="lightgrey")
	#Plot grids in the color of predicted class
	for c in range(1,n_com+1):
		com_color = cm.jet(c/float(n_com))
		#Plot grids with single predicted class in dark color
		DFsingle[DFsingle["prediction"]==c].plot(ax=base, markersize=1.5, color=com_color)
		#Plot grids with multiple predicted classes in light color
		DFmulti[DFmulti["prediction"]==c].plot(ax=base, markersize=1.5, color=com_color, alpha=0.3)
	ax.tick_params(labelsize=14)
	ax.set_xlabel("Longitude", fontsize=14)
	ax.set_ylabel("Latitude", fontsize=14)
	ax.set_title("{}/{}".format(month,year), fontsize=22)
	ax.set_aspect(0.5/ax.get_data_ratio())
	leg = ax.legend([mpatches.Patch(color=cm.jet(c/float(n_com))) for c in range(1,n_com+1)],
			  [str(c) for c in range(1,n_com+1)],
			  bbox_to_anchor=(1, 1),
			  loc="upper left",
			  fontsize=14)
	leg.set_title("Predicted\ncomm. type", prop={"size": 12, "weight": "heavy"})
	fig.subplots_adjust(left=0.12, right=0.82, top=0.9, bottom=0.17)

	#Save to a PNG file
	fig.savefig("../figures/{}/global/global.prediction.{}.{}.png".format(subdirec,year,month), format="png")
	plt.close(fig)

