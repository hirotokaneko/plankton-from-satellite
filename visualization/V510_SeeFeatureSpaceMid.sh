#!/bin/bash

opo2=`[ $2 = "all" ] && echo "" || echo "$2."`
tpr2=`[ $3 = "keep" ] && echo "" || echo "thinned$3."`

#python V511_SeeRandomSampleLocations.py $2 $5 > ../logs/V511_SeeRandomSampleLocations.$2.$5.log
#python V512_SeeUmap.py $1 $2 $3 $4 $5
#python V513_ClassOnUmap.py $1 $2 $3 $4 $5 $6
#python V514_ClassOnSST.py $1 $2 $3 $4 $6
#python V515_GenerateUmapSummary.py $1 $2 $3 $4 $5 $6
#python V516_UmapWithProvince.py $1 $2 $3 $4 $5
