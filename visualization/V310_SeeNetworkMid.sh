#!/bin/bash

opo2=`[ $2 = "all" ] && echo "" || echo "$2."`
tpr2=`[ $3 = "keep" ] && echo "" || echo "thinned$3."`
#mkdir ../figures/$1.${opo2}${tpr2}frq$4

#python V313_VisualizeNetwork.py $1 $2 $3 $4 $5

#mkdir ../figures/$1.${opo2}${tpr2}frq$4/community
#python V314_CommunityAnalysis.py $1 $2 $3 $4 $5

#python V315_SeeEdgeSatisfaction.py $1 $2 $3 $4 $5

#python V316_SeeClassLocations.py $1 $2 $3 $4 $5

#python V317_ClassDetectionSummary.py $1 $2 $3 $4 $5

#python V318_CommunityDetailSummary.py $1 $2 $3 $4 $5

#python V319_SpeciesBreakdownInCommunity.py $1 $2 $3 $4 $5

