# Note-Detection
Identifying notes on music sheets using Dijkstra's algorithm, Support Vector Machine

A 5 month coding journey involving numerous attempt to remove staffline (a common step in Optical Music Recognition (OMR) pipeline to detect/identify notes). There are numerous papers on this particular topic (OMR), but the novel approach of my approach is using methods from two papers (Cardoso et al., 2009), (Calvo-Zaragoza et al., 2016). A short description of each method is provided and more details are outlined in methods.md.

The former is the "shortest path" approach where we traverse the sheet music horiziontally by following dark pixels and incurring a penalty we choose a white pixel or decide to traverse in the y-direction (staff lines are horizontal). The latter approach is to use supervised machine learning algorthim to detect if a pixel belongs to staff line or non-staff line pixel category. The word "supervised" might be an issue and indeed it was an issue.. (I created my own dataset...)

# Raymond's OMR pipeline
The full OMR pipeline is a 5-step procedure outline as follows:
1) Staff line removal using Dijkstra's algorthim, SVM
2) Perform Density-Based Spatial Clustering of Application with Noise (DBSCAN) on the staff removed sheet music
3) Identify clusters of music elements and extract each element into its own separate sub image
4) Perform "bounding box" procedure on each music element (this step can be skipped)
5) Use SVM again to identify note heads on each music element

# Citations
1) J. dos Santos Cardoso, A. Capela, A. Rebelo, C. Guedes and J. Pinto da Costa, "Staff Detection with Stable Paths," in IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 31, no. 6, pp. 1134-1139, June 2009, doi: 10.1109/TPAMI.2009.34.
2) Calvo-Zaragoza, J., Micó, L. & Oncina, J. Music staff removal with supervised pixel classification. IJDAR 19, 211–219 (2016). https://doi.org/10.1007/s10032-016-0266-2
