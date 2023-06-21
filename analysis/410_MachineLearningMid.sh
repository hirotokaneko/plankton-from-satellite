#!/bin/bash
cd ../data

opo2=`[ $2 = "all" ] && echo "" || echo "$2."`
tpr2=`[ $3 = "keep" ] && echo "" || echo "thinned$3."`
s="$1.${opo2}${tpr2}frq$4"
feat_sel=('space' 'product' 'rrs' 'satellite' 'allfeat' 'sst' 'chl' 'par' 'duo' 'trio')

##------------------------------------
#mkdir $s/cv

#for f in "${feat_sel[@]}"; do
#	python ../scripts/411_CrossValidation.py $1 $2 $3 $4 $5 $6 $7 $f $8 $9 ${10} > ../logs/411_CrossValidation.$s.$5.$6.$7.$f.${10}.log
#done

#python ../scripts/412_GetAccuracy.py $1 $2 $3 $4 $5 $6 $7 ${10}

##-------------------------------------
#mkdir $s/fit

#for f in "${feat_sel[@]}"; do
#	python ../scripts/413_Fit.py $1 $2 $3 $4 $5 $6 $7 $f $8 $9  > ../logs/413_Fit.$s.$5.$6.$7.$f.log
#done

#:>$s/fit/fit.model.$5.$6.$7.txt
#for f in "${feat_sel[@]}"; do
#	echo $f >> $s/fit/fit.model.$5.$6.$7.txt
#	cat ../logs/413_Fit.$s.$5.$6.$7.$f.log >> $s/fit/fit.model.$5.$6.$7.txt
#done

