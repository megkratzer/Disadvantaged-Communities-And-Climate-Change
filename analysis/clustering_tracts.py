import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#read in data (use trimmed, not modeling since we want all columns individually - not a climate grouping)
df = pd.read_csv('../data/trimmed_data.csv')
df = df.set_index(['Census tract 2010 ID','County Name','State/Territory'])

#scale and impute data to prepare for pca and clustering
#also drop Underinvestment since it's almost entirely null
df = df.drop('Underinvestment',axis=1)
imputer = KNNImputer(n_neighbors=10)
scaler = RobustScaler()
X_imputed = imputer.fit_transform(df)
X_scaled = scaler.fit_transform(X_imputed)

#use pca to get dimensions to 2 for visuals, b
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

#%%
#create an elbow plot to determine optimal k
inertia = []
for k in range(1, 11):  # Change the range as needed
    kmeans = KMeans(n_clusters=k, random_state=123)
    kmeans.fit(X_pca)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Curve
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o')  # Change the range as needed
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

#there is a relatively clear elbow at 3

#%%
#perform k means with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=123)
kmeans.fit(X_pca)

#add labels to df
labels = kmeans.labels_
df['Cluster'] = labels

#plot the clusters
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis')  # Assuming you have at least 2 features
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=100, alpha=0.75)  # Plot the centroids
plt.title('Clusters and Centroids')
plt.tight_layout()
plt.savefig('../images/clusters.png')

#export to csv for later use in qgis
df.reset_index().to_csv('../data/clustered_data.csv', index=False)

