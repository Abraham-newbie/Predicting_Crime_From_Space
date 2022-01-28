[![Continuous Integration](https://github.com/OpenSourceEconomics/ose-scientific-computing-course-space_farers/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenSourceEconomics/ose-data-science-course-project-Abraham-newbie/actions/workflows/ci.yml) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ose-scientific-computing-course-space_farers/master?filepath=project_notebook.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/OpenSourceEconomics/ose-scientific-computing-course-space_farers/blob/master/project_notebook.ipynb)



# Prediction of Crime Rates using Brightness derived from Nighttime Satellite Light Images - VIIRS

---
OSE Scientific Computing | Winter 2021, M.Sc. in Economics, University of Bonn | [Sona Verdiyeva](https://github.com/s6soverd)() and [Abraham Raju](https://github.com/Abraham-newbie)(3296612)

---

This notebook contains derivation of brightness index from [VIIRS Nighttime Satellite Light Images](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG), and with the addition of other control variables, the prediction of crime rates in the city of Portland, Oregano state in US. As far as the brightness index concerns, the index is derived for all the neighborhoods in the city of Portland, for which the 'offense type and occurrence' datasets are available. 


## Overview of the Project:

Spatial Analysis of crime is the use of Geospatial Information to visualize the spatial data for explanatory statistical analysis and as well as with the purpose of identifying how certain factors (e.g, population characteristics, structural or ecological changes etc.) affect the spatial patterns of crime.  

This project focuses on the addition of brightness values derived from Nighttime Satellite Image Collection in predicting the number of crime occurrences that are more bound to happen during the night, and see whether the lights hold a predictive power over crime occurrence and if the effect can be replicated when taking into account controls for economic conditions. 

We also extend the project by using Call for Service data provided by the Portland police bureaue for geospatial prediction.<br>



## Additional Notes

The replication is conducted using R. Additional functions required to plot the graphs can be found in the auxiliary folder [here](https://github.com/OpenSourceEconomics/ose-scientific-computing-course-space_farers/tree/master/auxiliary) and plots/graphs which cannot be directly reproduced due to constraints of CI or github (e.g 3-d plots,dynamic plots) can be found in the files folder [here](https://github.com/OpenSourceEconomics/ose-scientific-computing-course-space_farers/tree/master/Figures).

The geo-spatial crime data can be downloaded [here](https://www.portlandoregon.gov/police/71978), and the call for service data can be downloaded here. [here](https://www.portlandoregon.gov/police/76454)



## Running the Notebook

To run this reproducible notebook,firstly clone the notebook and proceed as follows in your conda terminal.

> $ conda env create -f environment.yml

> $ conda activate space_farers

**The best way to view the notebook is to clone accordingly, or to view through nbviewer as tables and equations as well has html figures do not render well in github.**




---






