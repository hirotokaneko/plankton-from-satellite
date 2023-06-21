#!/bin/bash
cd ../data

opo2=`[ $2 = "all" ] && echo "" || echo "$2."`
tpr2=`[ $3 = "keep" ] && echo "" || echo "thinned$3."`
mkdir $1.${opo2}${tpr2}frq$4

#python ../scripts/311_HighPassFilter.py $1 $2 $3 $4

#mkdir flashweave
#julia -p 16 ../scripts/312_RunFlashWeave.jl $1 $2 $3 $4 $5 > ../logs/312_RunFlashWeave.$1.$2.$3.$4.$5.log

#cut -f 1 ../${direc}/asv.$1.filt.dd.grid.sat.${opo2}${tpr2}tsv | sed '1d' > flashweave/$1.${opo2}${tpr2}samplename
#sed -e '1,2d' flashweave/$1.${opo2}${tpr2}frq$4.$5.edgelist > ../data/$1.${opo2}${tpr2}frq$4/network.$1.${opo2}${tpr2}frq$4.$5.tsv
#python ../scripts/313_GetFlashWeaveResults.py $1 $2 $3 $4

#Rscript --vanilla ../scripts/314_CommunityDetection.R $1 $2 $3 $4 $5 > ../data/$1.${opo2}${tpr2}frq$4/modularity.$1.${opo2}${tpr2}frq$4.$5.txt

#python ../scripts/315_GetTaxonomy.py $1 $2 $3 $4

#python ../scripts/316_CalcEdgeSatisfaction.py $1 $2 $3 $4 $5

