import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams['figure.dpi'] = 300

#read in data 
df = pd.read_csv('../data/trimmed_data.csv')
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#correlation plot
corr_matrix = df.corr()
plt.figure(figsize=(20, 14)) 
#mask upper triangle
mask_upper = np.triu(np.ones_like(corr_matrix, dtype=bool))
#generate heatmap without annotations
sns.heatmap(corr_matrix, cmap='coolwarm', center=0, mask=mask_upper)
#annotate each cell
for i in range(len(corr_matrix)):
    for j in range(i + 1):
        plt.text(j + 0.5, i + 0.5, '{:0.2f}'.format(corr_matrix.iloc[i, j]),
                 horizontalalignment='center', verticalalignment='center', fontsize=10)
#format and save
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('../images/correlation_matrix.png')