import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import sys
import geopandas as gpd
from shapely.geometry import Point

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the list of grids
DFg = pd.read_csv("../input/eukbank_satellite_grid.tsv", delimiter="\t", index_col=0)
#Get the world map
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

#Loop by community detection methods
list_com_detec_met = ["fast_greedy","infomap","label_prop","leading_eigen",
					  "leiden","louvain","spinglass","walktrap"] 
for com_detec_met in list_com_detec_met:

	print("Method ->", com_detec_met)

	#Read the table of edge satisfaction index and representative community
	DFesf = pd.read_csv("../data/{}/edge.satisfaction.{}.{}{}frq{}.{}.{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ,NRM,com_detec_met), delimiter="\t", index_col=0)
	#Get the number of communities
	n_com = max(DFesf["class"])	

	#Add representative community to the list of grids
	DFcat = pd.concat([DFg, DFesf["class"]], axis=1, join="inner")
	#Convert into GeoDataFrame
	geometry = [Point(xy) for xy in zip(DFcat["GridLong"], DFcat["GridLat"])]
	DFcoords = gpd.GeoDataFrame(DFcat, crs="EPSG:4326", geometry=geometry)

	#Plot representative communities on the world map
	fig, ax = plt.subplots(figsize=(10,5))
	base = countries.plot(ax=ax, color="darkgrey")
	for c in range(1,n_com+1):
		com_color = cm.jet(c/float(n_com))
		DFcoords[DFcoords["class"]==c].plot(ax=base, markersize=15, color=com_color, edgecolor="dimgrey", linewidth=0.5, label=c)
	leg = ax.legend(bbox_to_anchor=(1, 1), loc="upper left", fontsize=16)
	leg.set_title("Community\ntype", prop={"size": 14, "weight": "heavy"})
	ax.tick_params(labelsize=14)
	ax.set_xlabel("Longitude", fontsize=16)
	ax.set_ylabel("Latitude", fontsize=16)
	fig.tight_layout()
	fig.savefig("../figures/{}/V316.class.map.{}.{}.png".format(subdirec,NRM,com_detec_met), format="png")
	fig.clf()
