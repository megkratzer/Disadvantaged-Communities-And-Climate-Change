# Disadvantaged Communities and Climate Change

## Abstract

The goal of this repository is to understand how climate change, health, housing, workforce development, and demographic factors interact to create disadvantaged communities, and further investigating which factors may lead to increased climate risk.

## Data

The data source for this project is the [Climate and Economic Justice Screening Tool](https://screeningtool.geoplatform.gov/en/), a government website associated with the CEQ designed to show which Census Tracts within the US states and territories are considered disadvantaged due to a variety of social, demographic, and economic factors. I included the Communities CSV in the data folder of this repository, but you will need to individually download the [shapefile](https://screeningtool.geoplatform.gov/en/downloads#3.42/41.21/-95.01) codebook since it is too big to upload into Github. 

Due to the large number of variables provided within this data, I decided to specifically focus on factors within the [categories of burdens](https://screeningtool.geoplatform.gov/en/methodology) provided of climate change, health, housing, and workforce development (as well as the census demographic information and disadvantaged status). The variables associated with each are as follows:

* Climate change: agricultural loss rate, building loss rate, population loss rate, projected flood risk, projected fire risk
* Health: asthma, diabetes, heart disease, low life expectancy
* Housing: historic underinvestment, housing cost, lack of green space, lack of indoor plumbing, lead paint
* Workforce development: linguistic isolation, low median income, poverty, unemployment

Also within the Data folder are some python scripts used to [clean the data](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/data/cleaning_data.py) and [aggregate tract data](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/data/by_state_county_data.py) up to county or state level for use in QGIS, as well as other CSVs containing intermittent stage data used throughout the analysis scripts (trimmed data, modelling data, and cluster assignments data). 

## Analysis and Images Descriptions

The analysis within this repository includes the following:

* Python script for [correlations](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/analysis/correlation.py), producing a [correlation heat map](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/correlation_matrix.png) for all variables
* Python script to create a [random forest model](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/analysis/random_forest.py) with a [feature importance plot](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/rf_feature_importances.png) for predicting climate risk and understanding which factors are most influential
* Combined python script for [factor analysis and clustering](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/analysis/factor_analysis_and_clustering.py) for census tracts. This generates a [factor loadings chart](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/factor_loadings.png) useful for determining which variables behave most similarly, as well as a clustering assignments csv and a 2D [clustering plot](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/clusters.png) using the first two factor loadings as X & Y variables
* Additionally, there is a QGIS file that uses the shapefile and clustering data, as well as aggregated county and state data, to create three map visualizations of the contiguous United States. The visualizations are included in the images folder and show the following:
    1. [Percent of tracts within each state that are considered disadvantaged](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/states_disadvantaged.png)
    2. [Percent of tracts within each county that are considered disadvantaged](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/counties_disadvantaged.png)
    3. [Climate Hazards Risk Index analysis showing the risk severity for each county](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/climate_hazards_risk_index.png): This map shows that the majority of the climate risk (calculated using expected population, building, and agriculure loss rates) is within a vertical center line of the United States. In order to understand why this is, I used the random forest feature importance mentioned above to determine which factors are most influencing climate risk
    4. [Clustered groupings of census tracts by similarity](https://github.com/megkratzer/Disadvantaged-Communities-and-Climate-Change/blob/main/images/tract_clusters.png): This map uses the clustering assignments to visually show tract groupings. This would be useful for governments (specifically at a state or county scale) to understand which of their communities are at risk of similar issues and create initiatives to provide help to multiple communities instead of working through one problem or one area at a time

## Results Discussion

### Random Forest

The feature importances from the random forest model showed that the most significant variable for predicting climate risk was percentage of land that is green space, followed by the percentage of houses that contain lead paint (pre 1960's housing), and the percentage of those of hispanic and latino descent in the tract.

![Random Forest Feature Importances](/images/rf_feature_importances.png)

* **Green Space**: Higher values might be associated with lower climate risk due to the benefits of vegetation and open land in reducing urban heat islands, improving air quality, and controlling surface runoff
* **Lead Paint**: The significance of this feature in predicting climate risk could be tied to older infrastructure's vulnerability to climate impacts like extreme weather, potentially leading to greater health risks as well as higher maintenance and retrofitting costs
* **Hispanic & Latino**: This feature reflects socio-economic factors that influence how different communities with different racial makeups experience and adapt to climate-related hazards, possibly due to disparities in housing quality, access to resources, or historical patterns of urban development

### Factor Analysis

Parallel analysis suggested that 11 factors is ideal for this dataset, and the resulting factor loadings are shown below. Although there are many significant variables that make up each factor, most can be defined by their top few loadings. For example:

* Factor 1: primarily white communities, also highly associated with longer expectancies
* Factor 2: represents the communities labelled as "disadvantaged"
* Factor 3: represents the primarily Native American tracts and the significant socioeconomic attributes attached to these communities
* Factor 4: communities with less health concerns as well as improved workforce situations

![Factor Loadings Heatmap](/images/factor_loadings.png)

### Clustering

The above factor loadings were used to determine clustering assignments for all tracts, and these clusters were then mapped in QGIS. On a national scale it is interesting to see the clusters somewhat match known similariies. For example, the cluster lines through the south east in pink and neon green, most of western Texas and southern New Mexico is clustered in blue, and a lot of the midwest is one green cluster. Possibly more important to local policy makers, however, are the cluster assignments that one might not expect. These clusters represent tracts that may have similar demographic makeups, but also show very similar climate, social, and economic status and therefore could aid policy makers to provide support to communities facing similar issues that they may not have thought to group together previously. 

![Clustering Assignments](/images/tract_clusters.png)