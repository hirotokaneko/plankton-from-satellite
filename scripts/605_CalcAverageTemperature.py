import numpy as np
import pandas as pd
import itertools

#Read the grid data
DFg = pd.read_csv("../input/all_satellite_grid.elev.minus.prov.tsv", delimiter="\t", index_col=0)
#Read the list of biomes
list_biomes = sorted(set(DFg["marine_biome"].dropna()))

#List of years and months
years = [2021] #for test
#years = np.arange(2003,2022)
months = np.arange(1,13)
list_yearmonths = ["{0}-{1:0=2}".format(year, month) for year, month in itertools.product(years, months)]

#Make a table for saving average temperatures
DFavetemp = pd.DataFrame(index=list_yearmonths, columns=list_biomes)

#Loop by years and months
for yearmonth in list_yearmonths:
	print(yearmonth)
        
	#Get year and month
	year = int(yearmonth.split("-")[0])
	month = int(yearmonth.split("-")[1])

	#Read satellite data of given month/year
	DFsat = pd.read_csv("../input/global/global_imputed_satellite_data.{}.{}.tsv".format(year,month), delimiter="\t", index_col=0)

	#Add satellite data to the grid data
	DFcat = pd.concat([DFg, DFsat.iloc[:,:-2]], axis=1, join="outer")
	#Add cosine of latitude (= relative area to equatorial grids)
	DFcat["Cosine"] = np.cos(np.deg2rad(DFcat["GridLat"]))

	#Loop by biomes
	for biome in list_biomes:
		#Extract data for given biome
		DFcat_biome = DFcat[DFcat["marine_biome"]==biome]
        
		#Caluculate total area
		tot_area = DFcat_biome["Cosine"].sum()
		#Calculate average temperature (weighted mean with realtive area)
		avetemp = (DFcat_biome["SST"]*DFcat_biome["Cosine"]).sum()/tot_area
		#Save to the table
		DFavetemp.loc[yearmonth,biome] = avetemp
        
#Save the table to a TSV file
DFavetemp.to_csv("average.temperature.tsv", sep="\t")

