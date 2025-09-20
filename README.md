Dockerfile created as a container for the streamlit app to be hosted on Google Cloud:

Link to Cloud Run site:

https://climate-app-670584475490.northamerica-northeast2.run.app/

# README for Climate Agriculture Impact

## Introduction

This project analyzes real-world climate, agriculture, CO₂ emission, and healthy diet datasets. The project looks to visualize and explore these datasets in concise and informative streamlit app.

This app (climate-app) will be hosted on Google Cloud Run here:

https://climate-app-670584475490.northamerica-northeast2.run.app/

![1758297167150](image/README/1758297167150.png)           ![1758297247003](image/README/1758297247003.png)

## Data

The data for this project comes from several different sources:

![1758303745328](image/README/1758303745328.png)

First a very large dataset from Our World in Data (OWID: https://ourworldindata.org/) the shows global CO₂ emissions since the year 1750. This contains data from every country in the world, it's a large CSV file that was downloaded directly from the site (full citation in [References](#references)).

![1758303779027](image/README/1758303779027.png)              ![1758303814353](image/README/1758303814353.png)

The next dataset comes from the Food and Agriculture Organization and World Bank (World Bank: https://data.worldbank.org/). This dataset shows the affordability of a healthy diet globally. It shows how many people are able to afford a healthy diet in each country. This was another CSV file downloaded directly from the site (full citation in [References](#references)).

![1758303866928](image/README/1758303866928.png)

The next dataset also comes from the World Bank but also the Climate Change Knowledge Portal (CCKP: https://climateknowledgeportal.worldbank.org/). This CSV was obtained through an API request, looking for a timeseries of annual rainfall from 1908-2024. The specific API request in found in the 'main_backup.ipynb' or 'CCKP_rainfall_data.ipynb' notebooks of this repo. A full citation come be found in [References](#references).

![1758303977816](image/README/1758303977816.png)     ![1758304019752](image/README/1758304019752.png)

Finally datasets of crop production of Canada and the United States of America were found at Statistics Canada (Stats Can: https://www.statcan.gc.ca/en/start) and the United States Department of Agriculture Quick Stats (USDA Quick Stats: https://www.nass.usda.gov/Quick_Stats/). These two datasets contains information on historical wheat and corn production that was used for this project. A full citation come be found in [References](#references).

## Methodology

This project required some extensive research to find the appropriate datasets. Once the research was complete the ETL (Extract, Transform, Load) process began in conjunction with EDA (Exploratory Data Analysis).

Other datasets and approaches were considered including FAO Aqua Stat (concerning globally water supply) and raster files precise regional crop production.


## Results

## Conclusion

## References

## Usage
