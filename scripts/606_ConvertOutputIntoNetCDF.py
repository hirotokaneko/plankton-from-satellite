import numpy as np
import numpy.ma as ma
import pandas as pd
import netCDF4 as nc
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

#Load coordinate table
DFco = pd.read_csv("../input/all_satellite_grid.tsv", delimiter="\t", index_col=0, dtype="object").astype(float)
DFco["RowInd"] = DFco["RowInd"].astype(int).astype(str)
DFco["ColInd"] = DFco["ColInd"].astype(int).astype(str)

#Make void table for mapped data
DFmap = pd.DataFrame(index=DFco["RowInd"].unique(), columns=DFco["ColInd"].unique())

#Range of years and months
years = np.arange(2003,2022)
#years = [2021] #for test
months = np.arange(1,13)

for year, month in itertools.product(years, months):
	print(year, month)

	#Read the table of the predicted class (= representative community) in given month/year
	DFp = pd.read_csv("{}/global/global.prediction.{}.{}.tsv".format(subdirec,year,month), delimiter="\t", index_col=0, dtype="object").astype(int)

	#Make mask for missing values
	DFmask = DFmap.copy()
	for co in DFp.index:
		rowind = DFco.loc[co,"RowInd"]
		colind = DFco.loc[co,"ColInd"]
		DFmask.loc[rowind, colind] = 0
	DFmask = DFmask.fillna(1)

	#Get prediction results
	dico_mx = {}
	for col in DFp.columns:
		DFpred = DFmap.copy()
		for co in DFp.index:
			rowind = DFco.loc[co,"RowInd"]
			colind = DFco.loc[co,"ColInd"]
			DFpred.loc[rowind, colind] = DFp.loc[co, col]
		mx = ma.masked_array(DFpred.values, mask=DFmask.values, fill_value=-1, dtype="float")
		dico_mx[col] = mx

	#Get long. and lat. arrays
	arrayLong = DFco["GridLong"].unique()
	arrayLat = DFco["GridLat"].unique()

	#Set cariable names
	dico_var_names = {col: "max_comm_type" if col=="prediction" else "comm_type_{}".format(col) for col in DFp.columns}
	dico_var_descs = {col: "Community type with max probability" if col=="prediction" else "Prediction of community type {}".format(col) for col in DFp.columns}

	#Write to NetCDF file
	with nc.Dataset("{}/global/pred_comm_types_{}_{}.nc".format(subdirec,year,month), "w", format="NETCDF4") as nc_data:
		
		#Create dimensions
		nc_data.createDimension("lon", len(arrayLong))
		nc_data.createDimension("lat", len(arrayLat))
		
		#Create long. and lat. variables
		lon = nc_data.createVariable("lon", "f4", "lon")
		lat = nc_data.createVariable("lat", "f4", "lat")
		lon[:], lat[:] = arrayLong, arrayLat
		
		#Create prediction result variables
		for col in DFp.columns:
			var_col = nc_data.createVariable(dico_var_names[col], "i4", ("lat", "lon"), fill_value=-1)
			var_col[:, :] = dico_mx[col]
			var_col.long_name = dico_var_descs[col]

print("finito")

