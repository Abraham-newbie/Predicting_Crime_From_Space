[![Continuous Integration](https://github.com/OpenSourceEconomics/ose-scientific-computing-course-space_farers/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenSourceEconomics/ose-data-science-course-project-Abraham-newbie/actions/workflows/ci.yml) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OpenSourceEconomics/ose-scientific-computing-course-space_farers/HEAD?urlpath=https%3A%2F%2Fgithub.com%2FOpenSourceEconomics%2Fose-scientific-computing-course-space_farers%2Fblob%2Fmaster%2Fproject_notebook.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/OpenSourceEconomics/ose-scientific-computing-course-space_farers/blob/master/project_notebook.ipynb)



# Prediction of Crime Rates using Brightness derived from Nighttime Satellite Light Images - VIIRS

---
OSE Scientific Computing | Winter 2021/22 | [Sona Verdiyeva](https://github.com/s6soverd) and [Abraham Raju](https://github.com/Abraham-newbie)

---

This notebook uses a relatively novel method of crime analysis, using nighttime-satellite data derived from [VIIRS Nighttime Satellite Light Images](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG) to predict and analyze crime and police response from geo-spatial data provided by the US city of Portland, Oregon.




## Overview of the Project:

Spatial Analysis of crime is the use of Geospatial Information to visualize the spatial data for explanatory statistical analysis and as well as with the purpose of identifying how certain factors (e.g, population characteristics, structural or ecological changes etc.) affect the spatial patterns of crime.  

This project focuses on the addition of brightness values derived from Nighttime Satellite Image Collection in predicting the number of crime occurrences that are more bound to happen during the night, and see whether the lights hold a predictive power over crime occurrence and if the effect can be replicated when taking into account controls for economic conditions. 

We also extend the project by using Call for Service data provided by the Portland police bureau for geospatial prediction and forecasting.<br>



## Additional Notes

This project was built using Python. Additional functions required to plot the graphs can be found in the auxiliary folder [here](https://github.com/OpenSourceEconomics/ose-scientific-computing-course-space_farers/tree/master/auxiliary) and plots/graphs which cannot be directly built due to constraints of CI or github (e.g 3-d plots,dynamic plots) can be found in the files folder [here](https://github.com/OpenSourceEconomics/ose-scientific-computing-course-space_farers/tree/master/Figures).

The Portland crime data can be downloaded [here](https://www.portlandoregon.gov/police/71978), and the geo-spatial call for service data can be downloaded [here](https://www.portlandoregon.gov/police/76454).



## Running the Notebook

To run this reproducible notebook,firstly clone the notebook and proceed as follows in your conda terminal.

> $ conda env create -f environment.yml

> $ conda activate space_farers

**The best way to view the notebook is to clone accordingly, or to view through nbviewer as tables and equations as well as html figures do not render well in github.**




---






