import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.impute import KNNImputer
import numpy as np
from sklearn.utils.extmath import randomized_svd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#load data
df = pd.read_csv('../data/modeling_data.csv')
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#create X and y datasets
y = df['climate_all']
X = df.drop('climate_all', axis=1)

#scale and impute data
imputer = KNNImputer(n_neighbors=10)
scaler = RobustScaler()
X_imputed = imputer.fit_transform(X)
X_scaled = scaler.fit_transform(X_imputed)

#%%
#decide the number of factors using parallel analysis

#define parallel analysis function
def perform_parallel_analysis(data, num_simulations=100, percentile=95):
    _, actual_sing_values, _ = randomized_svd(data, n_components=min(data.shape) - 1)
    random_sing_values = np.zeros((num_simulations, len(actual_sing_values)))

    for i in range(num_simulations):
        random_data = np.random.normal(0, 1, size=data.shape)
        _, sing_values, _ = randomized_svd(random_data, n_components=min(data.shape) - 1)
        random_sing_values[i, :] = sing_values

    sing_value_thresholds = np.percentile(random_sing_values, percentile, axis=0)
    actual_eigenvalues = actual_sing_values ** 2
    thresholds = sing_value_thresholds ** 2
    num_factors = np.sum(actual_eigenvalues > thresholds)
    
    return num_factors

num_factors = perform_parallel_analysis(X_scaled)
print("Number of factors suggested by Parallel Analysis:", num_factors)

#%%
#analyze factor loadings

n_factors = 6 #as suggested by parallel analysis above
fa = FactorAnalysis(n_components=n_factors, rotation='varimax')
fa.fit(X_scaled)

#%%
#turn factor loadings into df and view
loadings = fa.components_.T
loadings_df = pd.DataFrame(loadings, columns=['Factor {}'.format(i+1) for i in range(n_factors)], index=df.columns.drop('climate_all'))
print(loadings_df)

#plot loadings
plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(12, 10)) 
#create heatmap without annotations
sns.heatmap(loadings_df, cmap='coolwarm', center=0)
#add annotations
for (i, j), value in np.ndenumerate(loadings_df.values):
    plt.text(j + 0.5, i + 0.5, f"{value:.2f}", 
             ha='center', va='center', 
             fontsize=10)
plt.title('Factor Loadings')
plt.tight_layout()
plt.savefig('../images/factor_loadings.png')

#%%
#clustering with k means

#transform data
X_factor_scores = fa.transform(X_scaled)

#investigate elbow plot to determine k
inertia = []
for k in range(1, 11):  # Change the range as needed
    kmeans = KMeans(n_clusters=k, random_state=123)
    kmeans.fit(X_factor_scores)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Curve
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o')  # Change the range as needed
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.tight_layout()
plt.show()

#there is not a super clear elbow, but it looks like the graph begins to level off around k=5

#%%
#pick k of 5 
kmeans = KMeans(n_clusters=5, random_state=123)
kmeans.fit(X_factor_scores)

#add labels to df
labels = kmeans.labels_
df['Cluster'] = labels

#plot the clusters using the first two factors to visualize
plt.figure(figsize=(8, 6))
plt.scatter(X_factor_scores[:, 0], X_factor_scores[:, 1], c=labels, cmap='viridis') 
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=100, alpha=0.75)  # Plot the centroids
plt.title('Clusters and Centroids')
plt.tight_layout()
plt.savefig('../images/clusters.png')

#export to csv for later use in qgis
df.reset_index().to_csv('../data/clustered_data.csv', index=False)

