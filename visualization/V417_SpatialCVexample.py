import pandas as pd
import matplotlib.pyplot as plt
import sys
import geopandas as gpd
from shapely.geometry import Point

#Arguments
OPO = sys.argv[1]
TPR = sys.argv[2]
RAD = sys.argv[3]

#Read the list of grids
DFg = pd.read_csv("../input/eukbank_satellite_grid.tsv", delimiter="\t", index_col=0)
#Read the distance matrix of grids
DFd = pd.read_csv("../input/eukbank_grid_distance.tsv", delimiter="\t", index_col=0)
#Read the frequency table
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
DFf = pd.read_csv("../input/asv.small.filt.dd.grid.sat.{}{}tsv".format(opo2,tpr2), delimiter="\t", dtype="object", index_col=0)

#Extract the list of grids with frequency data
DFg2 = DFg.loc[DFf.index,:]
#Convert into GeoDataFrame
geometry = [Point(xy) for xy in zip(DFg2["GridLong"], DFg2["GridLat"])]
DFcoords = gpd.GeoDataFrame(DFg2, crs="EPSG:4326", geometry=geometry)

#Select a test sample
test_sample = "G0160"

#Samples outside buffer regions around the test sample
out_sample = DFd.index[DFd.loc[test_sample,:] > int(RAD)*1000]
#Training samples
train_sample = set(DFg2.index)&set(out_sample)
#Other samples (i.e. sampels inside buffer regions)
other_sample = set(DFg2.index)-set(train_sample)-set([test_sample])

#Convert map projection of GeoDataFrame to WGS 84 / UTM zone 26S (UTM for 30W-24W in the Southern Hemisphere)
DFcoords_utm = DFcoords.to_crs("EPSG:32726")
#Calculate buffer regions around each grid
DFcoords_buffer_utm = DFcoords_utm.buffer(distance=2000000)
#Revert map projection of buffer regions GeoDataFrame to WGS 84
DFcoords_buffer = DFcoords_buffer_utm.to_crs("EPSG:4326")

#Get the world map
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

#Plot test, training and other samples with buffer regions
fig, ax = plt.subplots(figsize=(10,5))
base = countries.plot(ax=ax, color="darkgrey")
gpd.GeoSeries(DFcoords_buffer.loc[test_sample]).plot(ax=base, color="paleturquoise")
gpd.GeoDataFrame(DFcoords.loc[test_sample,:]).T.plot(ax=base, marker="o", markersize=5, color="red", label="test")
DFcoords.loc[train_sample,:].plot(ax=base, marker="o", markersize=5, color="darkorange", label="train")
DFcoords.loc[other_sample,:].plot(ax=base, marker="o", markersize=5, color="darkgrey", label="neighbors")
ax.legend(bbox_to_anchor=(1.2,1))
fig.tight_layout()
fig.savefig("../figures/V417.{}{}sapatialCV.example.{}.png".format(opo2,tpr2,RAD), format="png")
fig.clf()
