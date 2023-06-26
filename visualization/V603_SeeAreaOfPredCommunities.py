import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymannkendall as mk
import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
BIM = sys.argv[5]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the area data
DFarea = pd.read_csv("../data/{}/explore/prediction.area.{}.tsv".format(subdirec,BIM), delimiter="\t", index_col=0, dtype="object").astype(float)
#Claculate moving average
DFarea_mean = DFarea.rolling(12).mean()

#Area of biomes (in 10^6 km2)
dico_real_area = {"Coastal": 37.39, "Polar": 20.78, "Westerlies": 129.93, "Trades": 139.90, "wholeocean": 328.00} 

#Make a subplots
fig, axes = plt.subplots(4, 2, figsize=(18,10), sharex=True)
#Loop by columns
for i, col in enumerate(DFarea.columns[:-1]):
	
	#Set subplot
	ax = axes[i//2,i%2]

	#Convert area into relative to total
	array_frac = dico_real_area[BIM]*(DFarea[col]/DFarea["TotArea"]).values
	array_frac_mean = dico_real_area[BIM]*(DFarea_mean[col]/DFarea_mean["TotArea"]).values

	#Trend test
	result = mk.seasonal_test(array_frac, period=1) #for test
	#result = mk.seasonal_test(array_frac, period=12)

	#Set position of timepoints
	array_timepoints = np.arange(DFarea.shape[0])
	#Bar plot for area of each month and line plot for moving average
	ax.bar(array_timepoints, array_frac, width=1.0, color="grey")
	ax.plot(array_timepoints, array_frac_mean, zorder=1, color="orange", linewidth="2")

	#Set tick and label of timepoints
	ax.tick_params(labelsize=14)
	ax.set_xticks(array_timepoints) #for test
	ax.set_xticklabels(np.arange(1,13)) #for test
	#ax.set_xticks([i for i in array_timepoints if i%12==6])
	#ax.set_xticklabels(np.arange(2003,2022), rotation=90)

	#Show trend test results
	ax.text(0.01, 0.99,
	 	"{0} (p = {1:.2g})\nSlope = {2:.3f} /year".format(result.trend, result.p, result.slope),
		verticalalignment="top", transform=ax.transAxes, fontsize=14)

	#Set title
	if col == "NoPrediction":
		tit = "No prediction"
	elif col == "Cloud":
		tit = "No satellite data"
	else:
		tit = "Community type {}".format(col)
	ax.set_title(tit, fontsize=18)

#Save the plot
fig.tight_layout()
fig.savefig("../figures/{}/explore/V603.prediction.area.{}.png".format(subdirec,BIM), format="png")
plt.close(fig)

