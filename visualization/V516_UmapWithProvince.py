import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.legend_handler import HandlerLine2D
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

#Set the satellite feature set
fts = "satellite"

#Read the UMAP projections
DFsc_emmb = pd.read_csv("../data/{}/umap/umap.random.{}.{}.tsv".format(subdirec, AAJ, fts), delimiter="\t", index_col=0)
DFeuk_sc_emmb = pd.read_csv("../data/{}/umap/umap.eukbank.{}.{}.tsv".format(subdirec, AAJ, fts), delimiter="\t", index_col=0)

#Read the table of province of random grids
DFprov = pd.read_csv("../input/random_satellite_grid.elev.minus.prov.tsv", delimiter="\t", index_col=0)

#List of grids existed both in UMAP projection and combined IHO province table (= not in lakes)
index_common = sorted(set(DFprov.index)&set(DFsc_emmb.index))
#Province table for existed grids
DFprov_sort = DFprov.loc[index_common,:]

#List of combined IHO provinces
list_oceans = sorted(set(DFprov["ocean"].dropna()))

#Visualize the UMAP projection colored by combined IHO provinces
fig, ax = plt.subplots(figsize=(9,5))
for i, ocean in enumerate(list_oceans):
    ind = DFprov_sort.index[DFprov_sort["ocean"] == ocean]
    X_sc_emmb = DFsc_emmb.loc[ind,:].values
    hnd = ax.scatter(X_sc_emmb[:,0], X_sc_emmb[:,1], color=cm.jet(i/6.), s=8, label=ocean, linewidths=.7, edgecolors=cm.jet(i/6.), alpha=.2)
Xeuk_sc_emmb = DFeuk_sc_emmb.values
hnd_euk = ax.scatter(Xeuk_sc_emmb[:,0], Xeuk_sc_emmb[:,1], s=25, c="mediumseagreen", linewidths=.7, edgecolors="darkgreen", zorder=10)
ax.set_xlabel("UMAP1", fontsize=16)
ax.set_ylabel("UMAP2", fontsize=16)
ax.tick_params(labelsize=14)
leg = ax.legend(bbox_to_anchor=(1.05,1), loc="upper left", fontsize=16, scatterpoints=20)
leg.set_title('Ocean', prop={'size': 14, 'weight': 'heavy'})
fig.tight_layout()
fig.savefig("../figures/{}/V516.umap.{}.{}.ocean.png".format(subdirec, AAJ, fts), format="png")
plt.close(fig)

#List of biomes
list_biomes = sorted(set(DFprov["marine_biome"].dropna()))

#Visualize the UMAP projection colored by Longhurst biome
fig, ax = plt.subplots(figsize=(9,5))
for i, biome in enumerate(list_biomes):
    ind = DFprov_sort.index[DFprov_sort["marine_biome"] == biome]
    X_sc_emmb = DFsc_emmb.loc[ind,:].values
    hnd = ax.scatter(X_sc_emmb[:,0], X_sc_emmb[:,1], color=cm.jet(i/3.), s=8, label=biome, linewidths=.7, edgecolors=cm.jet(i/3.), alpha=.2)
Xeuk_sc_emmb = DFeuk_sc_emmb.values
hnd_euk = ax.scatter(Xeuk_sc_emmb[:,0], Xeuk_sc_emmb[:,1], s=25, c="mediumseagreen", linewidths=.7, edgecolors="darkgreen", zorder=10)
ax.set_xlabel("UMAP1", fontsize=16)
ax.set_ylabel("UMAP2", fontsize=16)
ax.tick_params(labelsize=14)
leg = ax.legend(bbox_to_anchor=(1.05,1), loc="upper left", fontsize=16, scatterpoints=20)
leg.set_title('Longhurst\nbiome', prop={'size': 14, 'weight': 'heavy'})
fig.tight_layout()
fig.savefig("../figures/{}/V516.umap.{}.{}.biome.png".format(subdirec, AAJ, fts), format="png")
plt.close(fig)
