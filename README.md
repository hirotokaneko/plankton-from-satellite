# plankton-from-satellite
Scripts for constructing a machine learning model for the satellite-based prediction of the plankton community distributions.  
Plankton community types were identified from a inferred ecological network of plankton OTUs using a global metabarcoding dataset.

## Prerequisites
  * python (v3.8.7) - numpy (v1.19.4), pandas (v1.2.0), pyproj (v3.3.0), networkx (v2.5), scipy (v1.6.0), scikit-learn (v0.24.0), seaborn (v0.11.2), matplotlib (v3.5.1), geopandas (v0.10.2), shapely (v1.8.0), python-pptx (v0.6.21), pymannkendall (v1.4.2)
  * julia (v1.6.2) - FlashWeave (v0.18.0)
  * R (v3.6.1) - igraph (v1.2.11)

## Input files
Input files are in the directory `input`.
  * `asv.full.filt.dd.grid.sat.open.thinned200.frq20.tsv`: prepared metabarcoding data.
  * `eukbank_18SV4_asv.taxo.extracted`: taxonomic annotation of metabarcodes.
  * `eukbank_imputed_satellite_data.tsv`: prepared satellite data corresponded to sampling sites and times.
  * `eukbank_imputed_satellite_data.tsv/global` contains prepared satellite data (global and monthly) of 2021. Visit https://www.genome.jp/ftp/db/community/tara/Satellite/Data_and_Codes/01_DataProcessing/data/global/ for satellite data of 2003-2020.
  * other input files

Visit https://www.genome.jp/ftp/db/community/tara/Satellite/Data_and_Codes/01_DataProcessing/ for scripts used for generating input data.

## Scripts
Scripts for analyses are in the directory `scripts`.
  * `312_RunFlashWeave.jl`: a script for infering ecological network of plankton OTUs using FlashWeave.
  * `316_CalcEdgeSatisfaction.py`: a script for identification of community types from the network.
  * `411_CrossValidation.py`: a script for cross-validation of predictive models.
  * `602_GlobalPrediction.py`: a script for performing the prediction of plankton community distributions from satellite data.
  * other scripts

Scripts for generating figures are in the directory `visualization`.

Notes: You can follow the analysis flow by reading shell scripts (.sh). Please execute commands in shell scripts stepwize because they are not optimized for sequencial execution.

## Output files
Output data files will be generated in the directory `data` and figures will be generated in the directory `figure`.

Visit https://www.genome.jp/ftp/db/community/tara/Satellite/Output_NetCDF/ for NetCDF files of 19-year (2003-2021) time series of community type distribution predicted from satellite data.

## Contact
 - Hiroto Kaneko - kanekochem1994[@]icloud.com

## References
Kaneko H, Endo H, Henry N, Berney C, Mahé F, Poulain J, et al. Predicting global distributions of eukaryotic plankton communities from satellite data. ISME commun. 2023; 3:101. https://doi.org/10.1038/s43705-023-00308-7