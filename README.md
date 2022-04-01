# Key Commuting Routes
Please cite the following paper when using the code.  
Paper: *Wenbin Yao, Caijun Chen, Hongyang Su, Nuo Chen, Sheng Jin, Congcong Bai, "Analysis of Key Commuting Routes Based on Spatiotemporal Trip Chain", Journal of Advanced Transportation, vol. 2022, Article ID 6044540, 15 pages, 2022. https://doi.org/10.1155/2022/6044540*  

## Abstract
This code is a framework of key commuting routes mining algorithm based on license plate recognition(LPR) data.
Theoretically, the algorithm can be migrated to any similar spatio-temporal data, such as GPS trajectory data.
Commuting pattern vehicles are first extracted, and then the spatio-temporal trip chains of all commuting pattern vehicles are mined. 
Based on the spatio-temporal trip chains, the spatio-temporal similarity matrix is constructed by dynamic time warping (DTW) algorithm. 
The characteristics of commuting pattern are analysed by the density-based spatial clustering of applications with noise (DBSCAN) algorithm. 

## Content
```plain
  --    data_preprocess.py       extract car plates, trajectories and time series from raw LPR data
  --    clutering.py             use DBSCAN to cluster key routes
  --    DTW.py                   dynamic time warping (DTW) algorithm main functions
  --    matrix.py                calculate DTW matrices of sample group of commuting cars  
```