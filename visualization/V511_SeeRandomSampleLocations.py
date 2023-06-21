import pandas as pd
import matplotlib.pyplot as plt
import sys
import geopandas as gpd
from shapely.geometry import Point

#Arguments
OPO = sys.argv[1]
AAJ = sys.argv[2]

#Read the satellite data
DFsat = pd.read_csv("../data/random_imputed_satellite_data.4umap.{}.tsv".format(AAJ), delimiter="\t", index_col=0)
print("#grid cells: ", DFsat.shape[0])

#Convert into GeoDataFrame
geometry = [Point(xy) for xy in zip(DFsat["GridLong"], DFsat["GridLat"])]
DFcoords = gpd.GeoDataFrame(DFsat, crs="EPSG:4326", geometry=geometry)

#Get the world map
countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

#Plot random grids on the world map
fig, ax = plt.subplots(figsize=(10,5))
base = countries.plot(ax=ax, color="darkgrey")
DFcoords.plot(ax=base, marker="o", color="dimgrey", markersize=5)
ax.tick_params(labelsize=14)
ax.set_xlabel("Longitude", fontsize=16)
ax.set_ylabel("Latitude", fontsize=16)
fig.tight_layout()
opo2 = "" if OPO == "all" else "{}.".format(OPO)
fig.savefig("../figures/V511.{}random.{}.map.png".format(opo2, AAJ), format="png")
fig.clf()

