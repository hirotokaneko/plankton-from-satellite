#!/bin/bash

##$1=SIZ: data size
##$2=OPO: all or open ocean
##$3=TPR: thinning paramator (in km or keep)
##$4=FRQ: frequency threshold
##$5=NRM: normalization method
##$6=COM: community detection method
##$7=MLM: machine learning method
##$8=JOB: number of jobs
##$9=LIM: limit of iteration
##$10=RAD: radius for spatial cv

#./410_MachineLearningMid.sh full open 200 20 fz leiden NB 8 _ 0
#./410_MachineLearningMid.sh full open 200 20 fz leiden KNN 8 _ 0
#./410_MachineLearningMid.sh full open 200 20 fz leiden SVM 8 _ 0
#./410_MachineLearningMid.sh full open 200 20 fz leiden NN 8 12 0
#./410_MachineLearningMid.sh full open 200 20 fz leiden RF 8 _ 0

#./410_MachineLearningMid.sh full open 200 20 fz leiden NB 8 _ 2000
#./410_MachineLearningMid.sh full open 200 20 fz leiden KNN 8 _ 2000
#./410_MachineLearningMid.sh full open 200 20 fz leiden SVM 8 _ 2000
#./410_MachineLearningMid.sh full open 200 20 fz leiden NN 8 12 2000
#./410_MachineLearningMid.sh full open 200 20 fz leiden RF 8 _ 2000

