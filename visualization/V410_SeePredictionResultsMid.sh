#!/bin/bash

opo2=`[ $2 = "all" ] && echo "" || echo "$2."`
tpr2=`[ $3 = "keep" ] && echo "" || echo "thinned$3."`

#mkdir ../figures/$1.${opo2}${tpr2}frq$4/cv
#mkdir ../figures/$1.${opo2}${tpr2}frq$4/fit

#python V411_SeeCVresults.py $1 $2 $3 $4 $5 $6 $7 $8

#python V412_SeeFitResults.py $1 $2 $3 $4 $5 $6 $7

#python V413_SeeMapOfCV.py $1 $2 $3 $4 $5 $6 $7 $9 

#python V414_Metrics.py $1 $2 $3 $4 $5 $6 $7 $9

#python V415_CVsummary.py $1 $2 $3 $4 $5 $6 $7 $8

#python V416_FitSummary.py $1 $2 $3 $4 $5 $6 $7 $9

#python V417_SpatialCVexample.py $2 $3 $8

