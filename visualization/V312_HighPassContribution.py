import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib import cm

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]

#Set file name variables
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Read the frequency table after the selection of ASVs by frequency cutoff
DFf = pd.read_csv("../data/{}/asv.{}.filt.dd.grid.sat.{}{}frq{}.tsv".format(subdirec,SIZ,opo2,tpr2,FRQ), delimiter="\t", index_col=0, dtype="object").astype(int)

#----------------------
# Plot the total ASV frequency after the selection 
#----------------------

#Sum of ASV frequency values of each grid
SRsum = DFf.sum(axis=1)

#Bar plot of total ASV frequency
fig, ax = plt.subplots(figsize=(7,5))
ax.bar(SRsum.index, SRsum.values, width=1)
xticks = np.arange(0,len(SRsum),10)
ax.set_xticks(xticks)
ax.set_xticklabels(SRsum.index[xticks], rotation=90)
ax.set_xlabel("Grid")
ax.set_ylabel("Sum of ASV frequency")
fig.tight_layout()
fig.savefig("../figures/{}/V312.highpass.contribution.png".format(subdirec), format="png")
plt.close(fig)

#----------------------

#----------------------
# Plot taxonomic breakdown of ASVs before and after the selection 
#----------------------

#Function for plotting pie chart
def PlotTaxonomicBreakdown(asvs, figure_path, name, taxogroup):
	#Get index of taxonomies (top 8 + others, unclassified)
	SRtaxo_f = DFtaxo.loc[asvs,taxogroup]
	taxo_index = list(DFtaxo[taxogroup].value_counts().index[:8]) + ["others","unclassified"]
	colors = [cm.tab10(i) for i,j in enumerate(taxo_index)]
	#Count ASVs belonging each taxonomy
	count_sum = 0
	taxa_counts = []
	for taxa in taxo_index[:-2]:
		taxa_count = sum(SRtaxo_f==taxa)
		count_sum += taxa_count 
		taxa_counts.append(taxa_count)
	uncl_count = sum(SRtaxo_f!=SRtaxo_f)
	taxa_counts.append(SRtaxo_f.shape[0] - uncl_count - count_sum)
	taxa_counts.append(uncl_count)
	taxa_counts = np.array(taxa_counts)
	#Plot pie chart
	fig, ax = plt.subplots(figsize=(10,10))
	size = 0.20
	nz_ind = np.nonzero(taxa_counts)
	p, tx, autotexts = ax.pie(taxa_counts[nz_ind], radius=0.8-size, colors=np.array(colors)[nz_ind],
							labels=np.array(taxo_index)[nz_ind], pctdistance=0.8, autopct="", startangle=90,
							rotatelabels=True, textprops={"size":15}, wedgeprops=dict(width=size, edgecolor='w'))
	for i, a in enumerate(autotexts):
		a.set_text("{}".format(taxa_counts[nz_ind][i]))
	ax.axis('equal')
	fig.suptitle("{} taxa (n={})".format(name, SRtaxo_f.shape[0]), fontsize=24)
	fig.tight_layout()
	fig.savefig(figure_path, format="png")
	plt.close(fig)

#Read the taxonomy of ASVs
DFtaxo = pd.read_csv("../data/eukbank_18SV4_asv.taxo", delimiter="\t", index_col=0)

#Plot taxonomic breakdown of ASVs before the selection
figure_path = "../figures/{}/V312.taxonomy.breakdown.all.taxogroup1.png".format(subdirec)
PlotTaxonomicBreakdown(asvs=DFtaxo.index, figure_path=figure_path, name="All", taxogroup="taxogroup1")
figure_path = "../figures/{}/V312.taxonomy.breakdown.all.taxogroup2.png".format(subdirec)                                                                                                                                                   
PlotTaxonomicBreakdown(asvs=DFtaxo.index, figure_path=figure_path, name="All", taxogroup="taxogroup2")

#Plot taxonomic breakdown of ASVs after the selection 
figure_path = "../figures/{}/V312.taxonomy.breakdown.selected.taxogroup1.png".format(subdirec)
PlotTaxonomicBreakdown(asvs=DFf.columns, figure_path=figure_path, name="Selected", taxogroup="taxogroup1")
figure_path = "../figures/{}/V312.taxonomy.breakdown.selected.taxogroup2.png".format(subdirec)
PlotTaxonomicBreakdown(asvs=DFf.columns, figure_path=figure_path, name="Selected", taxogroup="taxogroup2")

#----------------------
