import sys

#Arguments
SIZ = sys.argv[1]
OPO = sys.argv[2]
TPR = sys.argv[3]
FRQ = sys.argv[4]
NRM = sys.argv[5]
COM = sys.argv[6]
MLM = sys.argv[7]
RAD = sys.argv[8]

#Define varibles
opo2 = "" if OPO == "all" else "{}.".format(OPO)
tpr2 = "" if TPR == "keep" else "thinned{}.".format(TPR)
subdirec = "{}.{}{}frq{}".format(SIZ,opo2,tpr2,FRQ)

#Collect accuracy scores
list_feature_set = ["space", "product", "rrs", "satellite", "allfeat", "sst", "chl", "par", "duo", "trio"]
list_acc = []

for fts in list_feature_set:
	with open("../logs/411_CrossValidation.{}.{}.{}.{}.{}.{}.log".format(subdirec,NRM,COM,MLM,fts,RAD), "r") as f:
		for line in f:
			if line[:13] == "Leave-one-out":
				elem = line.strip().split(" ")
				acc = float(elem[3])
				list_acc.append(acc)

#Write the table of accuracy scores
with open("{}/cv/accuracy.spatial{}.{}.{}.{}.txt".format(subdirec,RAD,NRM,COM,MLM), "w") as f:
	f.write("feature set\taccuracy\n")
	for i, fts in enumerate(list_feature_set):
		f.write("{}\t{}\n".format(fts,list_acc[i]))

