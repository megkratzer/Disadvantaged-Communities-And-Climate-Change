import pandas as pd

#read in original file - must specify string type for certain columns
df = pd.read_csv('../data/1.0-communities.csv', dtype={'Census tract 2010 ID':str,
                                                       'Identified as disadvantaged due to tribal overlap':str,
                                                       'Income data has been estimated based on geographic neighbor income':str,
                                                       'Does the tract have at least 35 acres in it?':str,
                                                       'Tract experienced historic underinvestment':str,
                                                       'Is there at least one abandoned mine in this census tract?':str,
                                                       'Names of Tribal areas within Census tract':str})

#set index to be census tract id
df = df.set_index('Census tract 2010 ID')

#view sample of the data
df.iloc[:,:3].head()


