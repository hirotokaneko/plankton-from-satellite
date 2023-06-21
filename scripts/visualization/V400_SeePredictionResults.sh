#!/bin/bash

##$1=SIZ: data size
##$2=OPO: all or open ocean
##$3=TPR: thinning paramator (in km or keep)
##$4=FRQ: frequency threshold
##$5=NRM: normalization method
##$6=COM: community detection method
##$7=MLM: machine learning method
##$8=RAD: radius for spatial cv
##$9=CTF: cutoff for probablistic output

#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden SVM 0 0.28


##only subscripts V411, V412, and V415 were executed in commands listed below:

#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden NB 0
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden KNN 0
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden NN 0
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden RF 0

#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden NB 2000
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden KNN 2000
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden SVM 2000
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden NN 2000
#./V410_SeePredictionResultsMid.sh full open 200 20 fz leiden RF 2000
