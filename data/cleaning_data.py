import pandas as pd

#read in original file - warnings are for unused columns 
df = pd.read_csv('../data/1.0-communities.csv', dtype={'Census tract 2010 ID':str})

#set index to be census tract id
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#columns to keep
#focusing on demographic info as well as Climate, Health, Housing, and Workforce Development Categories (as defined by data source)
keep = [
'Identified as disadvantaged'
,"Percent Black or African American alone"
,'Percent American Indian / Alaska Native'
,'Percent Asian'
,'Percent Native Hawaiian or Pacific'
,'Percent White'
,'Percent Hispanic or Latino'
,'Percent age under 10'
,'Percent age over 64'
,'Total population'

,'Expected agricultural loss rate (Natural Hazards Risk Index)'
,'Expected building loss rate (Natural Hazards Risk Index)'
,'Expected population loss rate (Natural Hazards Risk Index)'
,'Share of properties at risk of flood in 30 years'
,'Share of properties at risk of fire in 30 years'

,'Housing burden (percent)'
,'Median value ($) of owner-occupied housing units'
,'Tract experienced historic underinvestment'
, "Share of the tract's land area that is covered by impervious surface or cropland as a percent"
, 'Share of homes with no kitchen or indoor plumbing (percent)'
, 'Percent pre-1960s housing (lead paint indicator)'

,'Current asthma among adults aged greater than or equal to 18 years'
,'Diagnosed diabetes among adults aged greater than or equal to 18 years'
,'Coronary heart disease among adults aged greater than or equal to 18 years'
,'Life expectancy (years)'

,'Linguistic isolation (percent)'
,'Unemployment (percent)'
,'Is low income?'
,'Percent of individuals < 100% Federal Poverty Line'
,'Percent individuals age 25 or over with less than high school degree'
]

df = df[keep]

#rename columns for ease
names = {
'Identified as disadvantaged':'Disadvantaged'
,"Percent Black or African American alone":'African_American'
,'Percent American Indian / Alaska Native':'Native'
,'Percent Asian':'Asian'
,'Percent Native Hawaiian or Pacific':'Hawaiian_Pacific'
,'Percent White':'White'
,'Percent Hispanic or Latino':'Hispanic_Latino'
,'Percent age under 10':'Age<10'
,'Percent age over 64':'Age>64'
,'Total population':'Population'
,'Expected agricultural loss rate (Natural Hazards Risk Index)':'Agriculture_Loss'
,'Expected building loss rate (Natural Hazards Risk Index)':'Building_Loss'
,'Expected population loss rate (Natural Hazards Risk Index)':'Population_Loss'
,'Share of properties at risk of flood in 30 years':'Flood_Risk'
,'Share of properties at risk of fire in 30 years':'Fire_Risk'
,'Housing burden (percent)':'Housing_Burden'
,'Median value ($) of owner-occupied housing units':'House_Price'
,'Tract experienced historic underinvestment':'Underinvestment'
,"Share of the tract's land area that is covered by impervious surface or cropland as a percent":'Green_Space'
,'Share of homes with no kitchen or indoor plumbing (percent)': 'No_Plumbing'
,'Percent pre-1960s housing (lead paint indicator)': 'Lead_Paint'
,'Current asthma among adults aged greater than or equal to 18 years':'Asthma'
,'Diagnosed diabetes among adults aged greater than or equal to 18 years':'Diabetes'
,'Coronary heart disease among adults aged greater than or equal to 18 years':'Heart_Disease'
,'Life expectancy (years)':'Life_Expectancy'
,'Linguistic isolation (percent)':'Linguistic_Isolation'
,'Unemployment (percent)':'Unemployment'
,'Is low income?':'Low_Income'
,'Percent of individuals < 100% Federal Poverty Line':'Poverty'
,'Percent individuals age 25 or over with less than high school degree':'<HS_Diploma'
}

df = df.rename(columns=names)

df.to_csv('../data/trimmed_data.csv')
