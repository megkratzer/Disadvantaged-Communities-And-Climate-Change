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
plt.figure(figsize=(20, 14))  # Adjust size as needed
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f",annot_kws={"size": 8},mask=mask)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('../images/correlation_matrix.png')
