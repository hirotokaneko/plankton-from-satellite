import pandas as pd
import numpy as np
import pyproj

#Read grid data
DFg = pd.read_csv("../input/eukbank_satellite_grid.elev.prov.tsv", delimiter="\t", index_col=0)

#Extract coordinates
coordinates = DFg[["GridLat","GridLong"]].values

#Set the coordinate system
grs80 = pyproj.Geod(ellps="GRS80")
#For all samples...
list_distaces = []
for i in range(coordinates.shape[0]):
    #Make a vector of given coordinate
    stacoord = np.ones(shape=(coordinates.shape))
    stacoord = stacoord*coordinates[i]
    #Calculate distances between given coordinate and all coordinates
    _, _, distance = grs80.inv(stacoord[:,1], stacoord[:,0], coordinates[:,1], coordinates[:,0])
    list_distaces.append(distance)

#Convert distance matrix into dataframe
DFdist = pd.DataFrame(list_distaces, index=DFg.index, columns=DFg.index)
#Save dataframe
DFdist.to_csv("eukbank_grid_distance.tsv", sep="\t")
