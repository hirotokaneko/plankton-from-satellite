# plankton-from-satellite
Scripts for constructing a machine learning model for the satellite-based prediction of the plankton community distributions.  
Plankton community types were identified from a inferred ecological network of plankton OTUs using a global metabarcoding dataset.

## Input files
Input files are in the directory `input`.
  * `asv.full.filt.dd.grid.sat.open.thinned200.tsv`: prepared metabarcoding data.
  * `eukbank_18SV4_asv.taxo`: taxonomic annotation of metabarcodes.
  * `eukbank_imputed_satellite_data.tsv`: prepared satellite data corresponded to sampling sites and times.
  * other input files

Visit https://www.genome.jp/ftp/db/community/tara/Satellite/ for scripts used for generating input data.

## Output files
Output data files are in the directory `data`.
  * `full.open.thinned200.frq20/network.full.open.thinned200.frq20.fz.tsv`: inferred ecological network of plankton OTUs.
  * `full.open.thinned200.frq20/edge.satisfaction.full.open.thinned200.frq20.fz.leiden.tsv`: identified community types for each sample.
  * `full.open.thinned200.frq20/cv`: cross-validation results of predictive models.
  * `full.open.thinned200.frq20/global`: predicted community distribution data (2003-2021).
  * other output data files

Data visualizations are in the directory `figure`.
  * `full.open.thinned200.frq20/V317.summary.class.detection.fz.pptx`: summary of detected modules in the network.
  * `full.open.thinned200.frq20/V318.summary.community.detail.fz.pptx`: summary of the taxonomic breakdown of modules and the distribution of corresponded community types.
  * `full.open.thinned200.frq20/cv/V415.summary.CV.spatial0.fz.leiden.SVM.pptx`: summary of leave-one-out cross-validation results when using SVM.
  * `full.open.thinned200.frq20/cv/V415.summary.CV.spatial2000.fz.leiden.SVM.pptx`: summary of buffered cross-validation results when using SVM.
  * `full.open.thinned200.frq20/global`: visualization of the predicted community distributions (2003-2021).
  * other figures

## Scripts
Scripts for analyses are in the directory `analysis`.
  * `312_RunFlashWeave.jl`: a script for infering ecological network of plankton OTUs using FlashWeave.
  * `316_CalcEdgeSatisfaction.py`: a script for identification of community types from the network.
  * `411_CrossValidation.py`: a script for cross-validation of predictive models.
  * `602_GlobalPrediction.py`: a script for performing the prediction of plankton community distributions from satellite data.
  * other scripts

Scripts for visualization are in the directory `visualization`.

Notes: You can follow the analysis flow by reading shell scripts (.sh). Please execute commands in shell scripts stepwize because they are not optimized for sequencial execution.

## Contact
 - Hiroto Kaneko - kanekochem1994[@]icloud.com

## References
Hiroto Kaneko, Hisashi Endo, Nicolas Henry, Cédric Berney, Frédéric Mahé, Julie Poulain, Karine Labadie, Odette Beluche, Roy El Hourany, et al. 2022. Global observation of plankton communities from space. bioRxiv. https://www.biorxiv.org/content/10.1101/2022.09.23.508961v1
