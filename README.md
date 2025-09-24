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

The next dataset also comes from the World Bank but also the Climate Change Knowledge Portal (CCKP: https://climateknowledgeportal.worldbank.org/). This CSV was obtained through an API request, looking for a timeseries of annual rainfall from 1908-2024. The specific API request in found in the `main_backup.ipynb` or `CCKP_rainfall_data.ipynb` notebooks of this repo. A full citation come be found in [References](#references).

![1758303977816](image/README/1758303977816.png)     ![1758304019752](image/README/1758304019752.png)

Finally datasets of crop production of Canada and the United States of America were found at Statistics Canada (Stats Can: https://www.statcan.gc.ca/en/start) and the United States Department of Agriculture Quick Stats (USDA Quick Stats: https://www.nass.usda.gov/Quick_Stats/). These two datasets contains information on historical wheat and corn production that was used for this project. A full citation come be found in [References](#references).

## Methodology

Initial research centered on climate and agriculure datasets. This project consists of real-world data compiled from many sources (World Bank, OWID, FAO, USDA, etc. ) to a single PostgreSQL database hosted on RDS.

![1758742548180](image/README/1758742548180.png) ![1758742579823](image/README/1758742579823.png)

After initial research, an extensive ETL (extract, transform, load) and EDA (exploratory data analysis) stage began in VSCode by loading the datasets to with pandas to a jupyter notebook `.ipynb` file. 

Here each dataset was loaded into a single large notebook file to explore the data. 

Example (OWID):

![1758742951679](image/README/1758742951679.png)

Key columns were identified and unneccesary columns were dropped. However, this was still a preliminary and exploratory stage and final decisions were not made at this point. The purpose of this stage was to get to know the data, wide commonalities and decide how best to correlate the different datasets and coalesce them into a single database.

Example (OWID):

![1758742968008](image/README/1758742968008.png)

It was decided that the maximum range for this database would be the years 1908-2024. Some datasets contained much more than that, others much less. This date range was chosen to explore as much data as possible without overreaching.

Once all the datasets were successfully loaded into pandas, separate smaller `.ipynb` notebooks were created to to continue the ETL process. A full ETL pipeline was considered, however for the purposes of this project a single pipeline was not necessary. A separate notebook was created for each dataset (except for the Stats Can and USDA datasets). The idea was to create smaller single files to avoid a long scrolling single notebook for all the transformations. 

List of separate ETL files:

* CCKP rainfall file: `CCKP_rainfall_date.ipynb`
* FAO Healthy Diet Affordability file: `healthy_diet.ipynb`
* OWID CO₂ emissions file: `owid_date.ipynb`
* Stats Can and USDA crop files: `crop_date.ipynb`

## Results

## Conclusion

## References

## Usage
