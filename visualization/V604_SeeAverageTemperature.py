import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymannkendall as mk

#Read the average temperature data
DFavetemp = pd.read_csv("../data/average.temperature.tsv", delimiter="\t", index_col=0, dtype="object").astype(float)
#Claculate moving average
DFavetemp_mean = DFavetemp.rolling(12).mean()
#Get list of biomes
biomes = ["Polar", "Trades", "Westerlies"]

#Make a subplots
fig, axes = plt.subplots(3, 1, figsize=(9,7), sharex=True)
#Loop by biomes
for i, biome in enumerate(biomes):
	
	#Set subplot
	ax = axes[i]

	#Trend test
	result = mk.seasonal_test(DFavetemp[biome], period=1) #for test
	#result = mk.seasonal_test(DFavetemp[biome], period=12)

	#Set position of timepoints
	array_timepoints = np.arange(DFavetemp.shape[0])
	#Bar plot for area of each month and line plot for moving average
	ax.bar(array_timepoints, DFavetemp[biome], width=1.0, color="grey")
	ax.plot(array_timepoints, DFavetemp_mean[biome], zorder=1, color="orange", linewidth="2")

	#Set tick and label of timepoints
	ax.tick_params(labelsize=14)
	ax.set_xticks(array_timepoints) #for test
	ax.set_xticklabels(np.arange(1,13)) #for test
	#ax.set_xticks([i for i in array_timepoints if i%12==6])
	#ax.set_xticklabels(np.arange(2003,2022), rotation=90)

	#Set limits of y axis
	ymin = DFavetemp[biome].min()
	ymax = DFavetemp[biome].max()
	ax.set_ylim(ymin-1,ymax+1)
	#Show trend test results
	ax.text(0.01, 0.99,
	 		"{0} (p = {1:.2g})\nSlope = {2:.3f} /year".format(result.trend, result.p, result.slope),
			verticalalignment="top", transform=ax.transAxes, fontsize=14)
	#Set title
	ax.set_title(biome, fontsize=18)

#Save the plot
fig.tight_layout()
fig.savefig("../figures/V604.average.temperature.png", format="png")
plt.close(fig)
