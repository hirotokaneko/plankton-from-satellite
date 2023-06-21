import numpy as np
import pandas as pd
import itertools
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the grid data
DFg = pd.read_csv("../input/all_satellite_grid.elev.minus.prov.tsv", delimiter="\t", index_col=0)
#Read the list of biomes
list_biomes = sorted(set(DFg["marine_biome"].dropna()))
list_biomes += ["wholeocean"]

#List of years and months
#years = [2021] #for test
years = np.arange(2003,2022)
months = np.arange(1,13)
list_yearmonths = ["{0}-{1:0=2}".format(year, month) for year, month in itertools.product(years, months)]

#List of classes (= representative communities)
list_classes = [str(i+1) for i in range(6)]
#Dictionary of tables for saving area data
dico_areatables = {biome: pd.DataFrame(index=list_yearmonths, columns=list_classes+["NoPrediction", "Cloud", "TotArea"])
                   for biome in list_biomes}

#Loop by years and months
for yearmonth in list_yearmonths:
	print(yearmonth)
        
	#Get year and month
	year = int(yearmonth.split("-")[0])
	month = int(yearmonth.split("-")[1])

	#Read the table of the predicted class in given month/year
	DFp = pd.read_csv("{}/global/global.prediction.{}.{}.tsv".format(subdirec,year,month), delimiter="\t", index_col=0)
	#Add a column of the number of predicted calss for each grids 
	DFp["n_pred"] = DFp.iloc[:,:-1].sum(axis=1)

	#Add predicted class to the grid data
	DFcat = pd.concat([DFg, DFp], axis=1, join="outer")
	#Add cosine of latitude (= relative area to equatorial grids)
	DFcat["Cosine"] = np.cos(np.deg2rad(DFcat["GridLat"]))

	#Loop by biomes
	for biome in list_biomes:
		#Extract data for given biome
		if biome=="wholeocean":
			DFcat_biome = DFcat.copy()
		else:
			DFcat_biome = DFcat[DFcat["marine_biome"]==biome]
        
		#Caluculate area of each class
		pred_area = 0
		for c in list_classes:
			#Extract the table of given class
			DFcat_biome_c = DFcat_biome[DFcat_biome[c]==1]
			#Divide area (cosine) by the number of predicted calss
			SRarea_div = DFcat_biome_c["Cosine"]/DFcat_biome_c["n_pred"]
			c_area = SRarea_div.sum()
			#Save to the table
			dico_areatables[biome].loc[yearmonth,c] = c_area
			pred_area += c_area
		
		#Caluculate area of no prediction
		DFcat_biome_none = DFcat_biome[DFcat_biome["n_pred"]==0]
		none_area = DFcat_biome_none["Cosine"].sum()
		#Save to the table
		dico_areatables[biome].loc[yearmonth,"NoPrediction"] = none_area

		#Caluculate area of cloud (= no satellite data)
		DFcat_biome_cloud = DFcat_biome[DFcat_biome["n_pred"]!=DFcat_biome["n_pred"]]
		cloud_area = DFcat_biome_cloud["Cosine"].sum()
		#Save to the table
		dico_areatables[biome].loc[yearmonth,"Cloud"] = cloud_area

		#Caluculate total area
		tot_area = DFcat_biome["Cosine"].sum()
		#Save to the table
		dico_areatables[biome].loc[yearmonth,"TotArea"] = tot_area

		print("Residue:", tot_area - (pred_area + none_area + cloud_area)) #Should be close to zero

        
#Save the table to a TSV file
for biome in list_biomes:
	dico_areatables[biome].to_csv("{}/explore/prediction.area.{}.tsv".format(subdirec,biome), sep="\t")

