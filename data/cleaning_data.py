import pandas as pd

#read in original file - warnings are for unused columns 
df = pd.read_csv('../data/1.0-communities.csv', dtype={'Census tract 2010 ID':str})

#set index to be census tract id
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#columns to keep
keep = [
"Percent Black or African American alone"
,'Percent American Indian / Alaska Native'
,'Percent Asian'
,'Percent Native Hawaiian or Pacific'
,'Percent White'
,'Percent Hispanic or Latino'
,'Percent age under 10'
,'Percent age over 64'
,'Identified as disadvantaged'
,'Percentage of tract that is disadvantaged by area'
,'Share of neighbors that are identified as disadvantaged'
,'Total population'
,'Is low income?'
,'Expected agricultural loss rate (Natural Hazards Risk Index)'
,'Expected building loss rate (Natural Hazards Risk Index)'
,'Expected population loss rate (Natural Hazards Risk Index)'
,'Share of properties at risk of flood in 30 years'
,'Share of properties at risk of fire in 30 years'
,'Energy burden'
,'PM2.5 in the air'
,'Housing burden (percent)'
,'Median value ($) of owner-occupied housing units'
,'Tract experienced historic underinvestment'
,'Current asthma among adults aged greater than or equal to 18 years'
,'Diagnosed diabetes among adults aged greater than or equal to 18 years'
,'Coronary heart disease among adults aged greater than or equal to 18 years'
,'Life expectancy (years)'
,'Linguistic isolation (percent)'
,'Unemployment (percent)'
,'Percent of individuals < 100% Federal Poverty Line'
,'Percent individuals age 25 or over with less than high school degree'
]

df = df[keep]

#rename columns for ease
names = {
"Percent Black or African American alone":'African_American'
,'Percent American Indian / Alaska Native':'Native'
,'Percent Asian':'Asian'
,'Percent Native Hawaiian or Pacific':'Hawaiian_Pacific'
,'Percent White':'White'
,'Percent Hispanic or Latino':'Hispanic_Latino'
,'Percent age under 10':'<10'
,'Percent age over 64':'>64'
,'Identified as disadvantaged':'Disadvantaged'
,'Percentage of tract that is disadvantaged by area':'Area_Disadvantaged'
,'Share of neighbors that are identified as disadvantaged':'Neighbors_Disadvantaged'
,'Total population':'Population'
,'Is low income?':'Low_Income'
,'Expected agricultural loss rate (Natural Hazards Risk Index)':'Agriculture_Loss'
,'Expected building loss rate (Natural Hazards Risk Index)':'Building_Loss'
,'Expected population loss rate (Natural Hazards Risk Index)':'Population_Loss'
,'Share of properties at risk of flood in 30 years':'Flood_Risk'
,'Share of properties at risk of fire in 30 years':'Fire_Risk'
,'Energy burden':'Energy_Burden'
,'PM2.5 in the air':'Air_Pollution'
,'Housing burden (percent)':'Housing_Burden'
,'Median value ($) of owner-occupied housing units':'House_Price'
,'Tract experienced historic underinvestment':'Underinvestment'
,'Current asthma among adults aged greater than or equal to 18 years':'Asthma'
,'Diagnosed diabetes among adults aged greater than or equal to 18 years':'Diabetes'
,'Coronary heart disease among adults aged greater than or equal to 18 years':'Heart_Disease'
,'Life expectancy (years)':'Life_Expectancy'
,'Linguistic isolation (percent)':'Linguistic_Isolation'
,'Unemployment (percent)':'Unemployment'
,'Percent of individuals < 100% Federal Poverty Line':'Poverty'
,'Percent individuals age 25 or over with less than high school degree':'<HS_Diploma'
}

df = df.rename(columns=names)

df.to_csv('../data/trimmed_data.csv')
