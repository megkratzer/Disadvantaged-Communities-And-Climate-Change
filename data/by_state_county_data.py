#this script is going to group the data by state so we can export to qgis and plot

import geopandas as gpd

#read in tract shapefile
tracts = gpd.read_file('../data/usa.zip')

#keep only contiguous US states (the data includes other territories as well)
contiguous_us_states = [
    'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 
    'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
    'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 
    'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

# Filter the tracts GeoDataFrame to only include these states
tracts = tracts[tracts['SF'].isin(contiguous_us_states)]

#aggregate Natural Hazards Risk Index together (agricultural, building, and population loss rates)
tracts = tracts.copy()
tracts['Climate_Risk_Index'] = tracts['EALR_PFS'] + tracts['EBLR_PFS'] + tracts['EPLR_PFS']

#group by state and count num of total and disadvantaged tracts
state_data = tracts.groupby('SF').agg(
    Total_Tracts=('SN_C', 'count'),
    Disadvantaged_Tracts=('SN_C', 'sum'),
    Climate_Change_Factors=('Climate_Risk_Index', 'mean')
).reset_index()

#calculate percentage of disadvantaged tracts
state_data['Disadvantaged_Percentage'] = state_data['Disadvantaged_Tracts'] / state_data['Total_Tracts'] * 100

#dissolve geometry into state level
state_geometry = tracts.dissolve(by='SF')

#join summary data to state geometry
state_geometry = state_geometry.merge(state_data, on='SF')

#export state level to new shp
state_geometry.to_file('../data/dissolved_disadvantaged.gpkg', layer='states')
state_data.to_csv('../data/state_disadvantaged_percentage.csv', index=False)



#do the same analysis as above but by county level
county_data = tracts.groupby('CF').agg(
    Total_Tracts=('SN_C', 'count'),
    Disadvantaged_Tracts=('SN_C', 'sum')
).reset_index()

county_data['Disadvantaged_Percentage'] = county_data['Disadvantaged_Tracts'] / county_data['Total_Tracts'] * 100

county_geometry = tracts.dissolve(by='CF')

county_geometry = county_geometry.merge(county_data, on='CF')

county_geometry.to_file('../data/dissolved_disadvantaged.gpkg', layer='counties')
county_data.to_csv('../data/counties_disadvantaged_percentage.csv', index=False)
